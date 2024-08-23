import os
import re
import subprocess
import tempfile
from pathlib import Path
from typing import List, Optional

from pydejavu.utils.logger import Logger


class SpecParserSynthesizer:
    """Class to parse and synthesize QTL specifications using DejaVu's Verify tool.

    This class writes a given QTL specification to a temporary file, invokes the DejaVu tool
    to parse and synthesize it, and returns the output from the tool.
    """

    def __init__(self, i_dejavu_jar_path: Optional[str] = None, i_logger: Optional[Logger] = None):
        """
        Initializes the SpecParserSynthesizer with the path to the DejaVu JAR file.

        Args:
            i_dejavu_jar_path (str): The file path to the DejaVu JAR file. Defaults to 'libs/dejavu.jar'.
            i_logger (Logger, optional): A custom logger instance. If not provided, a new Logger is created.
        """
        self.__m_logger = Logger() if i_logger is None else i_logger
        self.__m_dejavu_jar_path = os.path.join(Path(__file__).resolve().parent.parent, 'libs', 'dejavu.jar')\
            if i_dejavu_jar_path is None else i_dejavu_jar_path
        self.__m_spec_names: List[str] = []

    @property
    def names(self) -> List[str]:
        return self.__m_spec_names

    def extract_spec_names(self, i_specification: str) -> None:
        """
        Extracts specification names from the given specification string.

        This method uses a regular expression to find all occurrences of
        "prop name:" in the specification string. It then stores the extracted
        names in the private __m_spec_names list.

        Args:
            i_specification (str): The input specification string containing
                                   one or more property definitions.
        Returns:
            None

        Raises:
            re.error: If there's an error in the regular expression pattern.
        """
        # Regular expression to match "prop name:" pattern
        pattern = r'prop\s+(\w+)\s*:'

        # Find all matches in the specification
        matches = re.findall(pattern, i_specification)

        # Store the matched names
        self.__m_spec_names = matches

    def parse_and_synthesize(self, i_specification: str) -> str:
        """
        Parses and synthesizes a QTL specification using the DejaVu tool.

        This method writes the provided QTL specification to a temporary file, then
        invokes the DejaVu Verify tool using the Java command. The tool's output is captured
        and returned.

        Args:
            i_specification (str): The QTL specification to parse and synthesize.

        Returns:
            str: The output from the DejaVu tool.

        Raises:
            RuntimeError: If the DejaVu tool encounters an error during execution.
        """

        # Extract spec names before processing
        self.extract_spec_names(i_specification)

        with tempfile.NamedTemporaryFile(mode='w', suffix='.qtl', delete=False) as spec_file:
            spec_file.write(i_specification)
            spec_file_path = spec_file.name

        cmd = [
            "java",
            "-cp", f".:{self.__m_dejavu_jar_path}",
            "dejavu.Verify",
            "--specfile", spec_file_path,
            "--execution", "1",
        ]

        try:
            stdout = subprocess.run(cmd, capture_output=True, text=True, check=True)
            return stdout.stdout

        except subprocess.CalledProcessError as e:
            error_message = (
                f"Error during parsing and synthesis: {e}\n"
                f"Command: {' '.join(cmd)}\n"
                f"Return code: {e.returncode}\n"
                f"Output: {e.stdout}\n"
                f"Error output: {e.stderr}"
            )
            raise RuntimeError(error_message) from e

        finally:
            try:
                os.unlink(spec_file_path)
            except OSError as e:
                self.__m_logger.warning(f"Failed to delete temporary spec file {spec_file_path}: {e}")


# Usage Example:
################
#
# if __name__ == "__main__":
#     parser_synthesizer = SpecParserSynthesizer()
#
#     specification = """
#     prop aaaaa : forall x . forall y . ((p(x, "true") & @q(y)) -> P r(x, y))
#     prop bbbbb : forall x . forall y . ((p(x, "true") & @q(y)) -> P r(x, y))
#     prop xxxxx : forall x . forall y . ((p(x, "true") & @q(y)) -> P r(x, y))
#     """
#
#     try:
#         result = parser_synthesizer.parse_and_synthesize(specification)
#         spec_names = parser_synthesizer.names
#         print("Parsing and synthesis result:")
#         print(result)
#         print(spec_names)
#     except Exception as e:
#         print(f"An error occurred: {e}")
