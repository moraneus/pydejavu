from typing import Callable, Dict, Any, List
from functools import wraps

from pydejavu.core.shared_state import SharedState
from pydejavu.utils.logger import Logger


class EventOperationalMapper:
    __slots__ = ['event_map', 'shared_state', '__m_logger']

    def __init__(self, i_logger: Logger = None):
        self.__m_logger = Logger() if i_logger is None else i_logger
        self.event_map: Dict[str, Callable] = {}
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

        def decorator(func: Callable[..., List[Any]]):
            @wraps(func)
            def wrapper(*args, **kwargs) -> List[Any]:
                self.__m_logger.debug(f"Executing event handler for {event_name}")
                result = func(*args, **kwargs)

                # Ensure the result is always a list
                if not isinstance(result, list):
                    return [result]
                return result

            self.event_map[event_name] = wrapper
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
