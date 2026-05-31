import csv
import logging
from typing import Any

from py_toolkit.exceptions import CsvParseError

logger = logging.getLogger(__name__)


def get_rows(file_path: str) -> list[dict[str, str]]:
    """Parse a CSV file into a list of dictionaries.

    Each dictionary maps column headers to row values.

    Args:
        file_path: Path to the CSV file.

    Returns:
        List of dictionaries, one per row.

    Raises:
        FileNotFoundError: If the file does not exist.
        CsvParseError: If the file cannot be parsed as CSV.

    Example:
        >>> rows = get_rows("data.csv")
        >>> rows[0]
        {'id': '1', 'name': 'alice', 'age': '30'}
    """
    rows: list[dict[str, str]] = []
    try:
        with open(file_path, "r") as file:
            for row in csv.DictReader(file):
                rows.append(row)
        logger.debug("Parsed %d rows from %s", len(rows), file_path)
        return rows
    except csv.Error as e:
        msg = f"Failed to parse CSV file {file_path}: {e}"
        logger.error(msg)
        raise CsvParseError(msg) from e
