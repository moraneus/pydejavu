import os
from enum import Enum
from pathlib import Path

import jnius_config

from pydejavu.utils.logger import Logger


class JarPaths(Enum):
    """Enumeration for JAR file paths."""

    SCALA = os.path.join(Path(__file__).resolve().parent.parent, 'libs', 'scala-library.jar')
    DEJAVU = os.path.join(Path(__file__).resolve().parent.parent, 'libs', 'dejavu.jar')


class JNIConfig:
    """Configuration class for setting up Java Native Interface (JNI) with custom options and classpath."""

    def __init__(self, i_logger: Logger = None):
        """
        Initializes the JNIConfig instance with default classpath and JVM options.

        The default classpath include the Scala and DejaVu JAR files. Additional JVM options for
        memory allocation are also set.

        Args:
            i_logger (Logger, optional): A custom logger instance. If not provided, a new Logger is created.
        """

        self.__m_logger = Logger() if i_logger is None else i_logger

        self.classpath = [
            JarPaths.SCALA.value,
            JarPaths.DEJAVU.value
        ]
        jnius_config.add_options('-Xms4g', '-Xmx16g')
        self.additional_paths = []
        self.java_opts = []

    def add_path(self, path: str) -> None:
        """
        Adds a path to the classpath if it exists.

        If the specified path does not exist, a warning is printed and the path is not added.

        Args:
            path (str): The path to a directory or JAR file to add to the classpath.
        """
        if os.path.exists(path):
            self.additional_paths.append(path)
        else:
            print(f"Warning: Path {path} does not exist and was not added to the classpath.")

    def set_heap_size(self, size: str) -> None:
        """
        Sets the maximum heap size for the Java Virtual Machine (JVM).

        This method appends a JVM option to set the maximum heap size, which is useful for controlling
        the memory allocation for the JVM.

        Args:
            size (str): A string representing the heap size (e.g., '4g' for 4 gigabytes).
        """
        self.java_opts.append(f'-Xmx{size}')

    def add_java_opt(self, opt: str) -> None:
        """
        Adds a custom Java option to the JVM options.

        This method allows you to specify additional JVM options as needed for your application.

        Args:
            opt (str): A string representing a Java option (e.g., '-Dsome.property=value').
        """
        self.java_opts.append(opt)

    def init_jnius_config(self) -> None:
        """
        Initializes the jnius configuration by setting the classpath and Java options.

        This method combines the default classpath, any additional paths, and any custom JVM options,
        and then applies them to the jnius configuration.
        """
        full_classpath = self.classpath + self.additional_paths
        jnius_config.set_classpath(*full_classpath)

        if self.java_opts:
            os.environ['JAVA_OPTS'] = ' '.join(self.java_opts)

    def check_heap_size(self) -> None:
        """
        Checks the maximum heap size allocated to the JVM and logs the information.

        This private method retrieves the maximum memory available to the JVM and logs a warning if it is
        less than 8GB. It also logs the current `JAVA_OPTS` environment variable.
        """
        from jnius import autoclass
        runtime = autoclass('java.lang.Runtime')
        max_memory = runtime.getRuntime().maxMemory()
        self.__m_logger.debug(f"Maximum heap size: {max_memory / (1024 * 1024):.2f} MB")

        if max_memory >= 8 * 1024 * 1024 * 1024:  # 8GB in bytes
            self.__m_logger.debug("Heap size successfully set to 8GB or more.")
        else:
            self.__m_logger.warning(f"Warning: Heap size is less than 8GB. "
                                    f"Actual size: {max_memory / (1024 * 1024 * 1024):.2f} GB")

        self.__m_logger.debug(f"JAVA_OPTS: {os.environ.get('JAVA_OPTS', 'Not set')}")
