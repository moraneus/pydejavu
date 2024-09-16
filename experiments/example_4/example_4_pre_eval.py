import argparse
import logging
import time
from typing import Tuple

from pydejavu.core.monitor import Monitor, event
from pydejavu.utils.benchmark_util import gtime


def parse_arguments() -> argparse.Namespace:
    """Parse command-line arguments for running the Dejavu Monitor.

    Returns:
        argparse.Namespace: The parsed arguments containing bits, logfile, and statistics flag.
    """
    parser = argparse.ArgumentParser(description="Run Dejavu Monitor with custom settings.")
    parser.add_argument(
        '-b', '--bits',
        type=int,
        default=20,
        help='Number of bits for the monitor (default: 20).'
    )
    parser.add_argument(
        '-l', '--logfile',
        type=str,
        required=True,
        help='CSV filename to read events from.'
    )
    parser.add_argument(
        '-s', '--stat',
        type=bool,
        default=False,
        help='Print statistics during evaluation (default: False).'
    )
    return parser.parse_args()


def initialize_monitor(bits: int, stat: bool) -> Monitor:
    """Initialize the Dejavu monitor with the specified parameters.

    Args:
        bits (int): Number of bits for the monitor.
        stat (bool): Flag to determine if statistics should be printed during evaluation.

    Returns:
        Monitor: An initialized instance of the Dejavu Monitor.
    """
    monitor = Monitor(i_bits=bits, i_statistics=stat, i_logging_level=logging.ERROR)

    # Due to the need to make minimum action for the experiments,
    # We used already compiled monitor
    monitor.linkage_monitor("example_4_trace_monitor.jar")
    return monitor


class State:
    def __init__(self):
        self.x = None
        self.q_args = set()
        self.y_plus_z = set()


def setup_event_handlers(monitor: Monitor):
    """Define and register event handlers for the Dejavu monitor."""

    state = State()

    @event("p")
    def handle_p(arg_x: int) -> Tuple[str, bool]:
        state.x = arg_x * 2
        calc_res = check_all_x_conditions(state, monitor.logger)
        return "p", calc_res

    @event("q")
    def handle_q(arg: int):

        # Add new sums with existing q_args
        if arg not in state.q_args:
            for existing_arg in state.q_args:
                state.y_plus_z.add(arg + existing_arg)

            # Add arg to q_args after calculating new sums
            state.q_args.add(arg)


def check_all_x_conditions(state: State, monitor_logger) -> bool:
    if not state.x or not state.y_plus_z:
        monitor_logger.info("One or more sets are empty; cannot perform calculation.")
        return False

    # Check if x are in y_plus_z
    if state.x not in state.y_plus_z:
        monitor_logger.info(f"No valid y, z found for x={state.x} where y != z.")
        return False

    monitor_logger.info("All x in X have valid y, z pairs in Y and Z that satisfy the formula where y != z.")
    return True


@gtime
def process_events(monitor: Monitor, filename: str) -> None:
    """Process events from the specified CSV file using the Dejavu monitor.

    Args:
        monitor (Monitor): The initialized Dejavu monitor instance.
        filename (str): The path to the CSV file containing events.

    Raises:
        FileNotFoundError: If the specified CSV file is not found.
        Exception: For any other unexpected errors during processing.
    """
    start_time = time.time()  # Start the timer
    try:
        for chunk in monitor.read_bulk_events_as_string(filename, chunk_size=100000):
            results = monitor.verify(chunk)
            monitor.logger.debug(f"Processed chunk of {len(chunk)} events")
            for result in results:
                monitor.logger.debug(str(result))
        monitor.end()
    except FileNotFoundError:
        print(f"Error: File {filename} not found.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    finally:
        end_time = time.time()  # End the timer
        elapsed_time = end_time - start_time
        print(f"Time taken to process events: {elapsed_time:.3f} seconds")


def main() -> None:
    """Main function to execute the Dejavu monitoring script."""
    # Parse command-line arguments
    args = parse_arguments()

    # Define the Dejavu specification
    specification = """
    prop origin: p("true")
    """

    # Initialize the Dejavu monitor
    monitor = initialize_monitor(args.bits, args.stat)

    # Setup event handlers
    setup_event_handlers(monitor)

    # Process events from the specified logfile
    process_events(monitor, args.logfile)


if __name__ == "__main__":
    main()
