import logging
from typing import Any, Tuple, List, Dict, Union

from pydejavu.core.monitor import Monitor, event, parser


# Define a custom event class
class CustomEvent:
    def __init__(self, name: str, args: List[Any]):
        self.__m_name = name
        self.__m_args = args

    @property
    def name(self):
        return self.__m_name

    @property
    def args(self):
        return self.__m_args

    def __repr__(self):
        return f"CustomEvent(name={self.name}, args={self.args})"


# Initialize the monitor with the updated specification
specification = """
prop suspicious_login : forall ip . forall user . ( successful_login(ip, user) -> ! P failed_in_row(ip, user) )
"""

monitor = Monitor(i_spec=specification, i_bits=16, i_logging_level=logging.INFO)


@parser("login")
def custom_login_parser(e: Dict[str, Union[CustomEvent, str]]) -> Tuple[str, List[Any], str]:
    """
    Custom parser for login events.

    Args:
        e (CustomEvent): The custom event format.

    Returns:
        Tuple[str, List[Any], str]: Parsed event in standard format.
    """
    event_name = e.get("name")
    event_args = e.get("data").args

    # Format original input for logging purposes
    origin_eval_input = f"{event_name},{','.join(map(str, event_args))}"

    return event_name, event_args, origin_eval_input


# Define global variables to track state
failed_attempts = {}


@event("login")
def handle_login(ip: str, user: str, success: bool):
    global failed_attempts
    if not success:
        failed_attempts[(ip, user)] = failed_attempts.get(
            (ip, user), 0) + 1
        if failed_attempts[(ip, user)] >= 3:
            return "failed_in_row", ip, user
        else:
            return None
    else:
        failed_attempts[(ip, user)] = 0
        return "successful_login", ip, user


# Example of processing an event stream using a custom format
events = [
    {"name": "login", "data": CustomEvent("login", ["192.168.1.10", "user1", False])},
    {"name": "login", "data": CustomEvent("login", ["192.168.1.10", "user1", False])},
    {"name": "login", "data": CustomEvent("login", ["192.168.1.10", "user1", False])},
    {"name": "login", "data": CustomEvent("login", ["192.168.1.10", "user1", True])},
    {"name": "#end#", "args": []}
]

# Process events using the monitor
for event in events:
    result = monitor.verify.process_event(event)
    print(result)
