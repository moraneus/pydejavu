import argparse
import logging
import subprocess
import sys
import time
from typing import List, Optional, Any, Callable, Iterator, Dict, Tuple

from pydejavu.compilation.scala_monitor_compiler import ScalaMonitorCompiler
from pydejavu.compilation.spec_parser_synthesizer import SpecParserSynthesizer
from pydejavu.jni.linkage_monitor import LinkageMonitor
from pydejavu.core.verify import Verify
from pydejavu.utils.file_utils import FileUtils
from pydejavu.utils.logger import Logger
from pydejavu.utils.monitor_generator import MonitorGenerator


class Monitor:
    """
    A singleton class for initializing and managing a DejaVu runtime monitor.

    This class handles the creation, synthesis, compilation, and linkage of runtime monitors
    based on the provided specifications. It also offers methods to handle events and manage
    shared variables in the runtime environment.

    Attributes:
        __instance (Monitor): The single instance of the Monitor class.
        __m_verify (Verify): The Verify object used for handling events and shared variables.
        __m_logger (Logger): The logger instance used for logging within the class.
        __pending_event_handlers (List[Tuple[str, Callable]]): List of events to be registered upon initialization.
    """

    __instance: Optional['Monitor'] = None  # Define the class-level instance attribute
    __pending_event_handlers: List[Tuple[str, Callable]] = []  # Store pending event handlers
    __pending_parser_handlers: List[Tuple[str, Callable]] = []  # Store pending parser handlers

    def __new__(cls, *args, **kwargs):
        if not cls.__instance:
            cls.__instance = super(Monitor, cls).__new__(cls)
            cls.__instance.__initialized = False
        return cls.__instance

    def __init__(
            self,
            i_spec: str = None,
            i_bits: int = 20,
            i_mode=None,
            i_statistics=False,
            i_logging_level: int = logging.INFO):
        """
        Initializes the Monitor instance with the given parameters.

        Args:
            i_spec (str, optional): The specification to be used for the monitor. Defaults to None.
            i_bits (int, optional): The number of bits used in verification. Defaults to 20.
            i_mode (optional): The mode of operation. Defaults to None.
            i_statistics (bool, optional): Whether to collect statistics. Defaults to False.
            i_logging_level (int): The logging level. Defaults to INFO level.
        """
        if self.__initialized:
            return
        self.__m_logger = Logger(i_logging_level=i_logging_level)
        self.__m_spec = i_spec
        self.__m_bits = i_bits
        self.__m_mode = i_mode
        self.__m_statistics = i_statistics
        self.__m_verify: Optional[Verify] = None

        # Register all pending events after initialization
        for event_name, func in self.__pending_event_handlers:
            self.register_event(event_name, func)
        self.__pending_event_handlers.clear()  # Clear pending events after registration

        # Register all pending parser after initialization
        for event_name, func in self.__pending_parser_handlers:
            self.register_parser(event_name, func)
        self.__pending_parser_handlers.clear()  # Clear pending processors after registration

        if self.__m_spec is not None:
            self.__init_monitor()
        self.__initialized = True

    @staticmethod
    def get_instance() -> 'Monitor':
        """
        Static method to get the singleton instance of the Monitor class.

        Returns:
            Monitor: The single instance of the Monitor class.
        """
        if Monitor.__instance is None:
            Monitor.__instance = Monitor()  # Create a new instance if it doesn't exist
        return Monitor.__instance

    @staticmethod
    def add_pending_event_handler(event_handler: Tuple[str, Callable]):
        """
        Static method to get the list of all pending events handlers for registration.

        Args:
            event_handler (Tuple[str, Callable]): The pending event operational handler for registration.
        """
        Monitor.__pending_event_handlers.append(event_handler)

    @staticmethod
    def add_pending_parser_handler(parser_handler: Tuple[str, Callable]):
        """
        Static method to get the list of all pending event parser for registration.

        Args:
            parser_handler (Tuple[str, Callable]): The pending event parser handler for registration.
        """
        Monitor.__pending_parser_handlers.append(parser_handler)

    @property
    def verify(self) -> Verify:
        """
        Returns the Verify object used for event handling and shared variable management.

        Returns:
            Verify: The Verify instance.
        """
        return self.__m_verify

    @property
    def logger(self) -> Logger:
        """
        Returns the logger instance used by this class.

        Returns:
            Logger: The logger instance.
        """
        return self.__m_logger

    def __init_monitor(self):
        """
        Initializes the monitor by synthesizing, compiling, and linking the specification.

        This method logs the steps of monitor creation and connects the monitor to the runtime.
        """
        self.__m_logger.info("Initialize monitor creation process")

        # Specification synthesizer process
        self.synthesize_monitor(self.__m_spec)

        # Synthesizer monitor compilation
        compile_jar_path = self.compile_monitor()

        # Connect to the compile monitor
        self.linkage_monitor(compile_jar_path)

    def synthesize_monitor(self, spec: str):
        """
        Synthesizes the monitor based on the provided specification.

        This method parses the specification and synthesizes the corresponding monitor. It logs the time
        taken for the process and the output of the synthesis.

        Args:
            spec (str): The specification string to be synthesized.
        """
        start_time = time.time()
        synthesizer = SpecParserSynthesizer(i_logger=self.__m_logger)
        parse_result = synthesizer.parse_and_synthesize(spec)
        synth_time = time.time() - start_time
        self.__m_logger.info(f"Specification synthesizer process completed in {synth_time: .2f} seconds")
        self.__m_logger.info(f"DejaVu Output: \n{parse_result}")

    def compile_monitor(self, source: Optional[str] = None) -> str:
        """
        Compiles the synthesized monitor into a JAR file.

        This method compiles the monitor and returns the path to the generated JAR file. It logs
        the time taken for the compilation.

        Args:
            source (str): Path to the scala source file that needs to be compiled

        Returns:
            str: The path to the compiled JAR file.
        """
        start_time = time.time()
        compiler = ScalaMonitorCompiler(i_source=source, i_logger=self.__m_logger)
        compile_jar_path = compiler.compile_monitor(generate_jar=True)
        compile_time = time.time() - start_time
        self.__m_logger.info(f"Synthesizer monitor compilation completed in {compile_time: .2f} seconds")
        return compile_jar_path

    def linkage_monitor(self, compile_jar_monitor: str) -> None:
        """
        Links the compiled dejavu_monitor to the runtime environment.

        This method initializes a LinkageMonitor with the compiled JAR file and sets up the
        verification environment.

        Args:
            compile_jar_monitor (str): The path to the compiled JAR file.
        """
        dejavu_monitor = LinkageMonitor(compile_jar_monitor)
        self.__m_verify = Verify(
            dejavu_monitor.monitor,
            i_bits=self.__m_bits,
            i_mode=self.__m_mode,
            i_statistics=self.__m_statistics)

        # Initialize the shared variables for the specification verdicts.
        # This is done by execute an "init" event which then return False for all defined properties
        self.__m_verify.process_event({"name": "#init#", "args": []})

    @staticmethod
    def read_bulk_events_as_dict(i_trace_file: str, chunk_size: int = 10000) -> Iterator[List[Dict[str, Any]]]:
        """
        Reads a large number of events from a trace file in chunks as dictionaries.

        This method uses the FileUtils to read events from the specified trace file. The events
        are read in chunks of dictionaries to manage memory efficiently.

        Args:
            i_trace_file (str): The path to the trace file.
            chunk_size (int, optional): The number of events to read in each chunk. Defaults to 10000.

        Yields:
            Iterator[List[Dict[str, Any]]]: An iterator yielding lists of dictionaries, where each dictionary
            represents an event with its name and associated arguments.
        """
        return FileUtils.read_events_from_file_as_dict(i_trace_file, chunk_size)

    @staticmethod
    def read_bulk_events_as_string(i_trace_file: str, chunk_size: int = 10000) -> Iterator[List[str]]:
        """
        Reads a large number of events from a trace file in chunks as strings.

        This method uses the FileUtils to read events from the specified trace file. The events
        are read in chunks of strings to manage memory efficiently, with each chunk being a list
        of strings, where each string represents a single row from the trace file.

        Args:
            i_trace_file (str): The path to the trace file.
            chunk_size (int, optional): The number of events to read in each chunk. Defaults to 10000.

        Yields:
            Iterator[List[str]]: An iterator yielding lists of strings, where each string represents
            a single row from the trace file.
        """
        return FileUtils.read_events_from_file_as_string(i_trace_file, chunk_size)

    def __is_initialized(self) -> bool:
        """
        Checks if the monitor is initialized.

        Returns:
            bool: True if initialized, False otherwise.
        """
        return self.__initialized

    @classmethod
    def event(cls, event_name: str) -> Callable:
        """
        A class method decorator to register an event handler with the monitor.

        If the monitor is initialized, it registers the event handler immediately.
        Otherwise, it stores the handler to be registered later when the monitor is initialized.

        Args:
            event_name (str): The name of the event to handle.

        Returns:
            Callable: The decorator function that registers the event handler.
        """

        def decorator(func: Callable):
            instance = cls.__instance
            if instance and instance.__is_initialized():
                instance.register_event(event_name, func)
            else:
                cls.__pending_event_handlers.append((event_name, func))  # Store event handler for later
            return func

        return decorator

    @classmethod
    def parser(cls, event_name: str) -> Callable:
        """
        Class method decorator to register an event parser with the monitor.

        If the monitor is initialized, it registers the parser immediately.
        Otherwise, it stores the parser to be registered later when the monitor is initialized.

        Args:
            event_name (str): The name of the event to process.

        Returns:
            Callable: The decorator function that registers the parser.
        """
        def decorator(func: Callable):
            instance = cls.__instance
            if instance and instance.__is_initialized():
                instance.register_parser(event_name, func)
            else:
                cls.__pending_parser_handlers.append((event_name, func))
            return func

        return decorator

    def register_event(self, event_name: str, func: Callable):
        """
        Registers an event handler with the Verify object.

        Args:
            event_name (str): The name of the event to handle.
            func (Callable): The function to handle the event.
        """
        self.__m_verify.event(event_name)(func)

    def register_parser(self, event_name: str, func: Callable):
        """
        Registers an event parser with the Verify object.

        Args:
            event_name (str): The name of the event to parse.
            func (Callable): The function to parse the event.
        """
        self.__m_verify.event_mapper.parser(event_name)(func)

    def get_shared(self, key: str, default: Any = None) -> Any:
        """
        Retrieves the value of a shared variable from the verification environment.

        Args:
            key (str): The key associated with the shared variable.
            default (Any, optional): The default value to return if the key is not found. Defaults to None.

        Returns:
            Any: The value of the shared variable.
        """
        return self.__m_verify.get_shared(key, default)

    def set_shared(self, key: str, value: Any) -> None:
        """
        Sets the value of a shared variable in the verification environment.

        Args:
            key (str): The key associated with the shared variable.
            value (Any): The value to set for the shared variable.
        """
        return self.__m_verify.set_shared(key, value)

    def end(self) -> None:
        """
        Notify the DejaVu that user need to ends its verification.
        This makes the result file to be closed correctly.
        It also called to get stat to summarize all events statistics.
        """
        self.__m_verify.end_eval()
        self.__m_verify.get_stat()

    def stat(self) -> None:
        """
        Get evaluation stat.
        The printed stat summarize all events until the moment it called.
        """
        self.__m_verify.get_stat()

    def last_eval(self, spec_name: str) -> Optional[bool]:
        """
        Retrieves the verdict of the last evaluation for a given property.

        This method fetches the verdict from the shared variables using the provided property name.
        If the property name is not found, an error is logged, a `KeyError` is raised, and the program exits.

        Args:
            spec_name (str): The name of the property whose verdict is being retrieved.

        Returns:
            Optional[bool]: The verdict of the last evaluation of the property, or None if the property is not found.

        Raises:
            KeyError: If the property name is not defined in the shared variables.
            SystemExit: If the property name is not found, the program will exit after logging the error.
        """
        verdict = self.get_shared(f"#last_eval_{spec_name}#", None)

        if verdict is None:
            self.__m_logger.error(
                f"Attempting to retrieve verdict for an undefined property '{spec_name}'. "
                f"Valid properties are: {self.__m_spec}."
            )

            # Exit the program after logging the error
            sys.exit(f"Exiting program due to undefined property '{spec_name}' name.")

        return verdict


# Define the global event function
def event(event_name: str) -> Callable:
    """
    A global decorator function to register an event handler with the monitor.

    If the monitor is initialized, it registers the event handler immediately.
    Otherwise, it stores the handler to be registered later when the monitor is initialized.

    Args:
        event_name (str): The name of the event to handle.

    Returns:
        Callable: The decorator function that registers the event handler.
    """
    monitor_instance = Monitor.get_instance()

    def decorator(func: Callable):
        if monitor_instance:
            monitor_instance.register_event(event_name, func)
        else:
            Monitor.add_pending_event_handler((event_name, func))  # Store event handler for later
        return func

    return decorator


# Global parser function
def parser(event_name: str) -> Callable:
    """
    A global decorator function to register an event parser with the monitor.

    If the monitor is initialized, it registers the event parser immediately.
    Otherwise, it stores the parser to be registered later when the monitor is initialized.

    Args:
        event_name (str): The name of the event to parser.

    Returns:
        Callable: The decorator function that registers the event parser.
    """

    monitor_instance = Monitor.get_instance()

    def decorator(func: Callable):
        if monitor_instance:
            monitor_instance.register_parser(event_name, func)
        else:
            Monitor.add_pending_parser_handler((event_name, func))
        return func

    return decorator


def execute_python_script(script_path):
    try:
        result = subprocess.run(['python3', script_path], check=True, capture_output=True, text=True)
        print("Script executed successfully.")
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print("An error occurred while executing the script:")
        print(e.stderr)


def main():
    # Set up argument parsing
    arg_parser = argparse.ArgumentParser(description='Generate and execute a Python script for PyDejaVu')
    arg_parser.add_argument('--bits', type=int, default=20, help='Number of bits for the monitor (default: 16)')
    arg_parser.add_argument('--stats', type=bool, default=False, help='Enable or disable statistics (default: False)')
    arg_parser.add_argument('--qtl', type=str, required=True, help='Path to the QTL file')
    arg_parser.add_argument('--operational', type=str, required=False, help='Path to the operational event handler file')
    arg_parser.add_argument('--trace', type=str, required=True, help='Path to the trace file')

    args = arg_parser.parse_args()

    # Generate the Python script based on the input files and parameters
    generated_script_path = MonitorGenerator.generate_python_script(
        qtl_path=args.qtl,
        pqtl_path=args.operational,
        trace_path=args.trace,
        bits=args.bits,
        stats=args.stats
    )

    # Execute the generated Python script
    execute_python_script(generated_script_path)


if __name__ == '__main__':
    main()
