import glob
import os
import subprocess
from pathlib import Path
from typing import Optional

from pydejavu.utils.logger import Logger


class ScalaMonitorCompiler:
    """
    A class to compile the synthesized monitor for DejaVu.
    """

    def __init__(
            self,
            i_dejavu: Optional[str] = None,
            i_source: Optional[str] = None,
            i_dest: str = "output",
            i_logger: Optional[Logger] = None):
        """
        Initialize the DejaVuMonitorCompiler.

        Args:
            i_dejavu (str): Path to the dejavu.jar file.
            i_source (str): Path to the scala source file that needs to be compiled
            i_dest (str): Path to the output directory containing TraceMonitor.scala.
            i_logger (Logger, optional): A custom logger instance. If not provided, a new Logger is created.
        """

        self.__m_logger = Logger() if i_logger is None else i_logger
        self.__m_dejavu_jar = os.path.join(Path(__file__).resolve().parent.parent, 'libs', 'dejavu.jar')\
            if i_dejavu is None else i_dejavu
        self.__m_dest = i_dest
        self.__m_compiled_jar_path = os.path.join(self.__m_dest, "TraceMonitor.jar")
        self.__m_source = os.path.join(self.__m_dest, "TraceMonitor.scala") if i_source is None else i_source

    @property
    def jar(self) -> str:
        return self.__m_compiled_jar_path

    def compile_monitor(self, generate_jar: bool = False) -> Optional[str]:
        """
        Compile the synthesized monitor.

        Args:
            generate_jar (bool): If True, generate a JAR file instead of class files.

        Returns:
            Optional[str]: Path to the compiled JAR file if generate_jar is True, None otherwise.

        Raises:
            subprocess.CalledProcessError: If compilation fails.
            FileNotFoundError: If TraceMonitor.scala is not found in the output directory.
        """

        if not os.path.exists(self.__m_source):
            raise FileNotFoundError(f"TraceMonitor.scala not found in {self.__m_dest}")

        res = None
        if generate_jar:
            res = self._compile_to_jar(self.__m_source)
        else:
            self._compile_to_class(self.__m_source)

        self.__cleanup()
        return res

    def _compile_to_class(self, trace_monitor_path: str) -> None:
        """
        Compile TraceMonitor.scala to class files.

        Args:
            trace_monitor_path (str): Path to TraceMonitor.scala file.

        Raises:
            subprocess.CalledProcessError: If compilation fails.
        """
        cmd = [
            "scalac",
            "-cp", f".:{self.__m_dejavu_jar}",
            trace_monitor_path
        ]

        try:
            subprocess.run(cmd, check=True, capture_output=True, text=True)
            self.__m_logger.info("Compilation successful. Class files generated in the output directory.")
        except subprocess.CalledProcessError as e:
            self.__m_logger.error(f"Compilation failed. Error: {e.stderr}")
            raise

    def _compile_to_jar(self, trace_monitor_path: str) -> str:
        """
        Compile TraceMonitor.scala to a JAR file.

        Args:
            trace_monitor_path (str): Path to TraceMonitor.scala file.

        Returns:
            str: Path to the compiled JAR file.

        Raises:
            subprocess.CalledProcessError: If compilation fails.
        """

        cmd = [
            "scalac",
            "-cp", f".:{self.__m_dejavu_jar}",
            trace_monitor_path,
            "-d", self.__m_compiled_jar_path
        ]

        try:
            subprocess.run(cmd, check=True, capture_output=True, text=True)
            self.__m_logger.info(f"Compilation successful. JAR file generated at: {self.__m_compiled_jar_path}")
            return self.__m_compiled_jar_path
        except subprocess.CalledProcessError as e:
            self.__m_logger.error(f"Compilation failed. Error: {e.stderr}")
            raise

    def __cleanup(self) -> None:
        """
        Remove all .class files in the current directory and the output directory.
        """
        # Remove .class files in the current directory
        for class_file in glob.glob("*.class"):
            os.remove(class_file)

        # # Remove .class files in the output directory
        # for class_file in glob.glob(os.path.join(self.output_dir, "*.class")):
        #     os.remove(class_file)

        self.__m_logger.info("Cleanup completed. All .class files have been removed.")


# Usage Example:
################
#
# if __name__ == "__main__":
#     dejavu_jar_path = "/path/to/dejavu.jar"
#     output_dir = "output"
#
#     compiler = ScalaMonitorCompiler(dejavu_jar_path, output_dir)
#
#     try:
#         # Compile to class files
#         compiler.compile_monitor()
#
#         # Or compile to JAR file
#         jar_path = compiler.compile_monitor(generate_jar=True)
#         if jar_path:
#             print(f"Compiled JAR file: {jar_path}")
#     except Exception as e:
#         print(f"An error occurred: {e}")
