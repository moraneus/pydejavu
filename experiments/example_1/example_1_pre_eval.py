import argparse
import logging
from typing import Tuple, Optional

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
    monitor.linkage_monitor("example_1_trace_monitor.jar")
    return monitor


def setup_event_handlers(dejavu: Monitor):
    """Define and register event handlers for the Dejavu monitor."""

    @event("q")
    def handle_q(arg_x: int, arg_y: int) -> Optional[Tuple[str | int, ...]]:
        if arg_y > 10:
            return "q", arg_x


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
    try:
        for chunk in monitor.read_bulk_events_as_string(filename, chunk_size=1000000):
            results = monitor.verify(chunk)
            monitor.logger.debug(f"Processed chunk of {len(chunk)} events")
            for result in results:
                monitor.logger.debug(str(result))
        monitor.end()
    except FileNotFoundError:
        print(f"Error: File {filename} not found.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


def main() -> None:
    """Main function to execute the Dejavu monitoring script."""
    # Parse command-line arguments
    args = parse_arguments()

    # Define the Dejavu specification
    specification = """
    prop modified: forall x . ( p(x) -> P q(x) )
    """

    # Initialize the Dejavu monitor
    monitor = initialize_monitor(args.bits, args.stat)

    # Setup event handlers
    setup_event_handlers(monitor)

    # Process events from the specified logfile
    process_events(monitor, args.logfile)


if __name__ == "__main__":
    main()
