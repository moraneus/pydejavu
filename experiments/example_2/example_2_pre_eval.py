import argparse
import time
from typing import List, Any, Tuple

from pydejavu.core.monitor import Monitor


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


def initialize_monitor(bits: int, specification: str, stat: bool) -> Monitor:
    """Initialize the Dejavu monitor with the specified parameters.

    Args:
        bits (int): Number of bits for the monitor.
        specification (str): The specification to initialize the monitor with.
        stat (bool): Flag to determine if statistics should be printed during evaluation.

    Returns:
        Monitor: An initialized instance of the Dejavu Monitor.
    """
    dejavu = Monitor(i_spec=specification, i_bits=bits, i_statistics=stat)
    dejavu.init_monitor()
    return dejavu


def setup_event_handlers(dejavu: Monitor):
    """Define and register event handlers for the Dejavu monitor."""

    @dejavu.operational("p")
    def handle_p(arg_x: int) -> Tuple[str | bool | int, ...]:
        return "p", arg_x, arg_x > 7


def process_events(dejavu: Monitor, filename: str) -> None:
    """Process events from the specified CSV file using the Dejavu monitor.

    Args:
        dejavu (Monitor): The initialized Dejavu monitor instance.
        filename (str): The path to the CSV file containing events.

    Raises:
        FileNotFoundError: If the specified CSV file is not found.
        Exception: For any other unexpected errors during processing.
    """
    start_time = time.time()  # Start the timer
    try:
        for chunk in dejavu.read_bulk_events_as_string(filename, chunk_size=1000):
            results = dejavu.verify.process_events(chunk)
            dejavu.logger.debug(f"Processed chunk of {len(chunk)} events")
            for result in results:
                dejavu.logger.debug(str(result))
        dejavu.verify.end_eval()
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
    prop modified: forall x . ((p(x, "true") -> exists y . @ q(x, y)))
    """

    # Initialize the Dejavu monitor
    dejavu = initialize_monitor(args.bits, specification, args.stat)

    # Setup event handlers
    setup_event_handlers(dejavu)

    # Process events from the specified logfile
    process_events(dejavu, args.logfile)


if __name__ == "__main__":
    main()
