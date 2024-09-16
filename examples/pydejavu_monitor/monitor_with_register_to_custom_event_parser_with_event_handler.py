import logging
from typing import Any, Tuple, List, Dict, Union

from pydejavu.core.monitor import Monitor, event, parser


# Define a custom event class
class LoginEvent:
    def __init__(self, username: str, ip: str, login_status: bool):
        self.__m_username = username
        self.__m_ip = ip
        self.__m_login_status = login_status

    @property
    def username(self):
        return self.__m_username

    @property
    def ip(self):
        return self.__m_ip

    @property
    def status(self):
        return str(self.__m_login_status).casefold()

    def __repr__(self):
        return f"{self.username},{self.ip},{self.status}"


# Initialize the monitor with the updated specification
specification = """
prop suspicious_login : forall ip . forall user . ( successful_login(ip, user) -> ! P failed_in_row(ip, user) )
"""

monitor = Monitor(i_spec=specification, i_bits=16, i_logging_level=logging.INFO)


@parser("login")
def custom_login_parser(event: Any) -> Tuple[str, List[Any], str]:
    """
    Custom parser for login events.

    Args:
        event (Any): The custom event format.

    Returns:
        Tuple[str, List[Any], str]: Parsed event in standard format.
    """
    event_name = event.get("name")
    login_event: LoginEvent  = event.get("data")
    username = login_event.username
    ip = login_event.ip
    status = login_event.status

    # Format original input for logging purposes
    origin_eval_input = f"{event_name},{str(login_event)}"

    return event_name, [username, ip, status], origin_eval_input


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
    {"name": "login", "data": LoginEvent("user1", "192.168.1.10", False)},
    {"name": "login", "data": LoginEvent("user1", "192.168.1.10", False)},
    {"name": "login", "data": LoginEvent("user1", "192.168.1.10", False)},
    {"name": "login", "data": LoginEvent("user1", "192.168.1.10", True)},
    {"name": "#end#", "args": []}
]

# Process events using the monitor
for event in events:
    result = monitor.verify.process_event(event)
    print(result)