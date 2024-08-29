from typing import Callable, Dict, Any, List, Tuple, Optional, Union
from functools import wraps

from pydejavu.core.shared_state import SharedState
from pydejavu.utils.logger import Logger


class EventOperationalMapper:
    __slots__ = ['event_map', 'parser_map', 'shared_state', '__m_logger']

    def __init__(self, i_logger: Logger = None):
        self.__m_logger = Logger() if i_logger is None else i_logger
        self.event_map: Dict[str, Callable] = {}
        self.parser_map: Dict[str, Callable[[Any], Tuple[str, List[Any], str]]] = {}
        self.shared_state = SharedState()
        self.__m_logger.info("EventOperationalMapper instance initialized")

    def event(self, event_name: str):
        """
        Decorator for registering event handlers.

        Args:
            event_name (str): The name of the event.

        Returns:
            callable: The decorator function.
        """

        def decorator(func: Callable[..., Optional[Union[Tuple[str, ...], List[Union[str, int, bool]], None]]]):
            @wraps(func)
            def wrapper(*args, **kwargs) -> Optional[Union[Tuple[str, ...], List[Union[str, int, bool]], None]]:
                self.__m_logger.debug(f"Executing event handler for {event_name}")
                result = func(*args, **kwargs)

                # Allow None as a valid return value
                if result is None:
                    return result

                # Check if the result is a tuple
                if isinstance(result, tuple):
                    # Ensure the first element is a string
                    if not result or not isinstance(result[0], str):
                        raise TypeError("The first item of the return tuple must be a string.")
                    return result

                # Check if the result is a list
                if isinstance(result, list):
                    # Ensure the first element is a string
                    if not result or not isinstance(result[0], str):
                        raise TypeError("The first item of the return list must be a string.")
                    return result

                # If result is neither a tuple, list, nor None, raise an error
                raise TypeError("The return value must be a tuple, list, or None.")

            self.event_map[event_name] = wrapper
            return wrapper

        return decorator

    def parser(self, event_name: str):
        """
        Decorator for registering event parser handlers.

        Args:
            event_name (str): The name of the event.

        Returns:
            callable: The decorator function.
        """

        def decorator(func: Callable[[Any], Tuple[str, List[Any], str]]):
            @wraps(func)
            def wrapper(event: Any) -> Tuple[str, List[Any], str]:
                self.__m_logger.debug(f"Executing parser for event '{event_name}'")
                return func(event)

            self.parser_map[event_name] = wrapper
            self.__m_logger.info(f"Custom event parser registered for event '{event_name}'")
            return wrapper

        return decorator

    def get_shared(self, key: str, default: Any = None):
        """
        Get a shared variable.

        Args:
            key (str): The key of the shared variable.
            default (Any): The default value if the key doesn't exist.

        Returns:
            Any: The value of the shared variable.
        """
        return self.shared_state.get(key, default)

    def set_shared(self, key: str, value: Any):
        """
        Set a shared variable.

        Args:
            key (str): The key of the shared variable.
            value (Any): The value to set.
        """
        self.shared_state.set(key, value)
