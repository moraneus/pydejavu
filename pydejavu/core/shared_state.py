from typing import Dict, Any
from collections import defaultdict


class SharedState:
    """A class to manage shared state using a dictionary with default values."""

    __slots__ = ['_data']

    def __init__(self):
        """
        Initializes the SharedState instance.

        The internal dictionary `_data` is initialized with a default value of `None`
        for any key that doesn't exist. This prevents KeyError exceptions when accessing
        keys that haven't been set.
        """
        self._data: Dict[str, Any] = defaultdict(lambda: None)

    def set(self, key: str, value: Any) -> None:
        """
        Sets the value for a given key in the shared state.

        Args:
            key (str): The key to set in the shared state.
            value (Any): The value to associate with the key.
        """
        self._data[key] = value

    def get(self, key: str, default: Any = None) -> Any:
        """
        Retrieves the value associated with a given key from the shared state.

        If the key is not found, the method returns the provided default value
        or `None` if no default is specified.

        Args:
            key (str): The key to retrieve from the shared state.
            default (Any, optional): The value to return if the key is not found. Defaults to `None`.

        Returns:
            Any: The value associated with the key, or the default value if the key is not found.
        """
        return self._data.get(key, default)

    def delete(self, key: str) -> None:
        """
        Deletes a key and its associated value from the shared state.

        If the key does not exist, the method does nothing.

        Args:
            key (str): The key to delete from the shared state.
        """
        self._data.pop(key, None)
