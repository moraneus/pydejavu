import logging
import os
from typing import Optional
from datetime import datetime


class Logger:
    """Singleton Logger class for handling application logging.

    This Logger class ensures that only one instance of the logger is created, providing
    consistent logging across the entire application. It sets up both console and file
    logging handlers with a predefined log format. The log file name includes a timestamp
    to ensure uniqueness.
    """

    _instance: Optional['Logger'] = None

    def __new__(cls, i_name: str = "PyDejaVu", i_logging_level: int = logging.INFO) -> 'Logger':
        """
        Creates a new instance of the Logger class if it doesn't already exist.

        This method ensures that only one instance of the Logger class is created (Singleton pattern).
        If an instance already exists, it returns that instance.

        Args:
            i_name (str): The name of the logger. Defaults to 'PyDejaVu'.
            i_logging_level (int): The logging level. Defaults to INFO level.

        Returns:
            Logger: The single instance of the Logger class.
        """
        if cls._instance is None:
            cls._instance = super(Logger, cls).__new__(cls)
            cls._instance._logger = logging.getLogger(i_name)
            cls._instance._setup_logger(i_logging_level)
        return cls._instance

    def _setup_logger(self, logging_level: int = logging.INFO) -> None:
        """
        Sets up the logger with console and file handlers.

        This private method configures the logger to output log messages to both the console
        and a dynamically named file using a consistent format that includes the timestamp,
        logger name, log level, and message.

        Args:
            logging_level (int): The logging level. Defaults to INFO level.
        """
        self._logger.setLevel(logging_level)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

        # Console core
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        self._logger.addHandler(console_handler)

        # Ensure the logs directory exists
        logs_dir = 'logs'
        os.makedirs(logs_dir, exist_ok=True)

        # File core with dynamic filename based on the current timestamp
        timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        log_filename = os.path.join(logs_dir, f'{timestamp}.log')
        file_handler = logging.FileHandler(log_filename)
        file_handler.setFormatter(formatter)
        self._logger.addHandler(file_handler)

        # Prevent log messages from being handled by the root logger
        self._logger.propagate = False

    def debug(self, message: str) -> None:
        """
        Logs a debug message.

        Args:
            message (str): The message to log.
        """
        self._logger.debug(message)

    def info(self, message: str) -> None:
        """
        Logs an informational message.

        Args:
            message (str): The message to log.
        """
        self._logger.info(message)

    def warning(self, message: str) -> None:
        """
        Logs a warning message.

        Args:
            message (str): The message to log.
        """
        self._logger.warning(message)

    def error(self, message: str) -> None:
        """
        Logs an error message.

        Args:
            message (str): The message to log.
        """
        self._logger.error(message)

    def critical(self, message: str) -> None:
        """
        Logs a critical message.

        Args:
            message (str): The message to log.
        """
        self._logger.critical(message)
