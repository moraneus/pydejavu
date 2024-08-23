
from pydejavu.jni.jni_config import JNIConfig
from pydejavu.utils.logger import Logger


class LinkageMonitor:
    """Class for monitoring linkage using JNI configuration and custom logging."""

    def __init__(self, i_monitor_jar: str, i_logger: Logger = None):
        """
        Initializes the LinkageMonitor instance.

        This constructor sets up logging, configures JNI settings, and initializes the monitor.

        Args:
            i_monitor_jar (str): The path to the monitor JAR file.
            i_logger (Logger, optional): A custom logger instance. If not provided, a new Logger is created.
        """
        self.__m_logger = Logger() if i_logger is None else i_logger
        self.__m_jni_config = JNIConfig()
        self.__m_monitor = self.__initialize_monitor(i_monitor_jar)

    @property
    def monitor(self):
        """
        Returns the initialized monitor.

        Returns:
            The monitor instance initialized through JNI.
        """
        return self.__m_monitor

    def __initialize_monitor(self, *paths: str):
        """
        Initializes the JNI configuration and sets up the monitor class.

        This private method adds the provided paths to the JNI classpath, initializes the JNI configuration,
        and loads the `TraceMonitor` class.

        Args:
            *paths (str): Paths to JAR files or directories to add to the classpath.

        Returns:
            monitor: The initialized monitor class from the JNI environment.
        """
        for path in paths:
            self.__m_jni_config.add_path(path)
        self.__m_jni_config.init_jnius_config()

        from jnius import autoclass
        monitor = autoclass('TraceMonitor')

        self.__m_logger.info("Initializes the JNI configuration and sets up the monitor class")

        # Check if heap size settings were applied
        self.__m_jni_config.check_heap_size()

        return monitor

