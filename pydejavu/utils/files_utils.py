from typing import Dict, Any, Iterator, List
import csv


class FileUtils:
    """Utility class for handling files operations."""

    @staticmethod
    def read_events_from_file(filename: str, chunk_size: int = 10000) -> Iterator[List[Dict[str, Any]]]:
        """
        Reads events from a CSV file in chunks.

        This method reads events from a specified CSV file and returns them in chunks of dictionaries,
        each containing the event's name and associated arguments.

        Args:
            filename (str): The path to the CSV file containing event data.
            chunk_size (int, optional): The number of events to include in each chunk. Defaults to 10,000.

        Yields:
            Iterator[List[Dict[str, Any]]]: An iterator yielding lists of dictionaries, where each dictionary
            represents an event with its name and arguments.

        Example:
            Suppose a CSV file contains the following rows:
                event1,arg1,arg2
                event2,arg1,arg2,arg3

            The method would yield chunks of events in the following format:
            [
                {"name": "event1", "args": ["arg1", "arg2"]},
                {"name": "event2", "args": ["arg1", "arg2", "arg3"]}
            ]
        """
        with open(filename, 'r') as file:
            reader = csv.reader(file)
            chunk = []
            for row in reader:
                if row:
                    event = {"name": row[0], "args": row[1:]}
                    chunk.append(event)
                    if len(chunk) >= chunk_size:
                        yield chunk
                        chunk = []
            if chunk:
                yield chunk

    @staticmethod
    def read_events_from_file_as_dict(filename: str, chunk_size: int = 10000) -> Iterator[List[Dict[str, Any]]]:
        """
        Reads events from a CSV file in chunks.

        This method reads events from a specified CSV file and returns them in chunks of dictionaries,
        each containing the event's name and associated arguments.

        Args:
            filename (str): The path to the CSV file containing event data.
            chunk_size (int, optional): The number of events to include in each chunk. Defaults to 10,000.

        Yields:
            Iterator[List[Dict[str, Any]]]: An iterator yielding lists of dictionaries, where each dictionary
            represents an event with its name and arguments.

        Example:
            Suppose a CSV file contains the following rows:
                event1,arg1,arg2
                event2,arg1,arg2,arg3

            The method would yield chunks of events in the following format:
            [
                {"name": "event1", "args": ["arg1", "arg2"]},
                {"name": "event2", "args": ["arg1", "arg2", "arg3"]}
            ]
        """
        with open(filename, 'r') as file:
            reader = csv.reader(file)
            chunk = []
            for row in reader:
                if row:
                    event = {"name": row[0], "args": row[1:]}
                    chunk.append(event)
                    if len(chunk) >= chunk_size:
                        yield chunk
                        chunk = []
            if chunk:
                yield chunk

    @staticmethod
    def read_events_from_file_as_string(filename: str, chunk_size: int = 10000) -> Iterator[List[str]]:
        """
        Reads events from a CSV file in chunks as strings.

        This method reads events from a specified CSV file and returns them in chunks of strings,
        where each string represents a row in the CSV file.

        Args:
            filename (str): The path to the CSV file containing event data.
            chunk_size (int, optional): The number of rows to include in each chunk. Defaults to 10,000.

        Yields:
            Iterator[List[str]]: An iterator yielding lists of strings, where each string is a row from the CSV file.

        Example:
            Suppose a CSV file contains the following rows:
                event1,arg1,arg2
                event2,arg1,arg2,arg3

            The method would yield chunks of events in the following format:
            [
                "event1,arg1,arg2",
                "event2,arg1,arg2,arg3"
            ]
        """
        with open(filename, 'r') as file:
            reader = csv.reader(file)
            chunk = []
            for row in reader:
                if row:
                    # Convert the row list to a comma-separated string
                    row_string = ','.join(row)
                    chunk.append(row_string)
                    if len(chunk) >= chunk_size:
                        yield chunk
                        chunk = []
            if chunk:
                yield chunk
