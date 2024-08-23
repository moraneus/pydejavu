import sys
import time
from typing import List, Optional, Any, Callable

from pydejavu.compilation.scala_monitor_compiler import ScalaMonitorCompiler
from pydejavu.compilation.spec_parser_synthesizer import SpecParserSynthesizer
from pydejavu.utils.files_utils import FileUtils
from pydejavu.jni.linkage_monitor import LinkageMonitor
from pydejavu.core.verify import Verify
from pydejavu.utils.logger import Logger


class Monitor:
    """
    A class for initializing and managing a DejaVu runtime monitor.

    This class handles the creation, synthesis, compilation, and linkage of runtime monitors
    based on the provided specifications. It also offers methods to handle events and manage
    shared variables in the runtime environment.

    Attributes:
        __m_verify (Verify): The Verify object used for handling events and shared variables.
        __m_logger (Logger): The logger instance used for logging within the class.

    Args:
        i_spec (str, optional): The specification to be used for the monitor. Defaults to None.
        i_bits (int, optional): The number of bits used in verification. Defaults to 20.
        i_mode (optional): The mode of operation. Defaults to None.
        i_statistics (bool, optional): Whether to collect statistics. Defaults to False.
        i_logger (Logger, optional): A custom logger instance. Defaults to None.
    """

    def __init__(self, i_spec: str = None, i_bits: int = 20, i_mode=None, i_statistics=False, i_logger: Logger = None):
        """
        Initializes the PyDejaVu instance with the given parameters.

        Args:
            i_spec (str, optional): The specification to be used for the monitor. Defaults to None.
            i_bits (int, optional): The number of bits used in verification. Defaults to 20.
            i_mode (optional): The mode of operation. Defaults to None.
            i_statistics (bool, optional): Whether to collect statistics. Defaults to False.
            i_logger (Logger, optional): A custom logger instance. Defaults to None.
        """
        self.__m_logger = Logger(i_name=__name__) if i_logger is None else i_logger
        self.__m_spec = i_spec
        self.__m_bits = i_bits
        self.__m_mode = i_mode
        self.__m_statistics = i_statistics
        self.__m_verify: Optional[Verify] = None

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

    def init_monitor(self):
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
        Links the compiled monitor to the runtime environment.

        This method initializes a LinkageMonitor with the compiled JAR file and sets up the
        verification environment.

        Args:
            compile_jar_monitor (str): The path to the compiled JAR file.
        """
        monitor = LinkageMonitor(compile_jar_monitor)
        self.__m_verify = Verify(
            monitor.monitor,
            i_bits=self.__m_bits,
            i_mode=self.__m_mode,
            i_statistics=self.__m_statistics)

        # Initialize the shared variables for the specification verdicts.
        # This is done by execute an "init" event which then return False for all defined properties
        self.__m_verify.process_event({"name": "#init#", "args": []})

    @staticmethod
    def read_bulk_events(i_trace_file: str, chunk_size: int = 10000):
        """
        Reads a large number of events from a trace file in chunks.

        This method uses the FileUtils to read events from the specified trace file. The events
        are read in chunks to manage memory efficiently.

        Args:
            i_trace_file (str): The path to the trace file.
            chunk_size (int, optional): The number of events to read in each chunk. Defaults to 10000.

        Returns:
            List[Any]: A list of events read from the file.
        """
        return FileUtils.read_events_from_file(i_trace_file, chunk_size)

    def operational(self, event_name: str) -> Callable:
        """
        Creates a handler function for the specified event.

        This method returns a callable that can be used to handle the event with the given name
        during the runtime.

        Args:
            event_name (str): The name of the event to handle.

        Returns:
            Callable: A function to handle the specified event.
        """
        return self.__m_verify.event(event_name)

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
