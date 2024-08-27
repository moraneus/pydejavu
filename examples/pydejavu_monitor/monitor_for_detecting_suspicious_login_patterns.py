import logging

from pydejavu.core.monitor import Monitor, event

# Define the refined specification with temporal constraint
specification = """
prop suspicious_login : forall ip . forall user . ( successful_login(ip, user) -> ! P failed_in_row(ip, user) )
"""

# Initialize the monitor with the updated specification
monitor = Monitor(i_spec=specification, i_bits=16, i_logging_level=logging.INFO)
monitor.init_monitor()

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


# Example of processing an event stream
events = [
    {"name": "login", "args": ["192.168.1.10", "user1", "False"]},
    {"name": "login", "args": ["192.168.1.10", "user1", "False"]},
    {"name": "login", "args": ["192.168.1.10", "user1", "False"]},
    {"name": "login", "args": ["192.168.1.10", "user1", "True"]},
    {"name": "#end#", "args": []}
]

# Process events using the monitor
for event in events:
    monitor.verify.process_event(event)
