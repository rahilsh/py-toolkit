import json
import logging
from typing import Any

from py_toolkit.exceptions import MissingOptionalDependencyError, XmlError

logger = logging.getLogger(__name__)

try:
    import xmltodict  # type: ignore[import-untyped]
except ModuleNotFoundError:  # pragma: no cover
    xmltodict = None  # type: ignore[assignment]


def file_get_contents(filename: str) -> str:
    """Read the entire contents of a text file.

    Args:
        filename: Path to the file.

    Returns:
        File contents as a single string.

    Raises:
        FileNotFoundError: If the file does not exist.

    Example:
        >>> content = file_get_contents("data.xml")
    """
    with open(filename) as f:
        return f.read()


def parse_xml(xml_content: str) -> dict[str, Any]:
    """Parse an XML string into a Python dictionary.

    Args:
        xml_content: XML string to parse.

    Returns:
        Dictionary representation of the XML.

    Raises:
        MissingOptionalDependencyError: If xmltodict is not installed.
        XmlError: If parsing fails.

    Example:
        >>> parse_xml("<root><item>value</item></root>")
        {'root': {'item': 'value'}}
    """
    if xmltodict is None:
        raise MissingOptionalDependencyError(
            "xmltodict is not installed. Install it with: pip install py-toolkit[xml]"
        )
    try:
        parsed = xmltodict.parse(xml_content)
        logger.debug("Parsed XML content (%d chars)", len(xml_content))
        return parsed
    except Exception as e:
        msg = f"Failed to parse XML: {e}"
        logger.error(msg)
        raise XmlError(msg) from e


def xml_file_to_json(filepath: str) -> str:
    """Read an XML file and convert it to a JSON string.

    Args:
        filepath: Path to the XML file.

    Returns:
        JSON string representation of the XML content.

    Raises:
        MissingOptionalDependencyError: If xmltodict is not installed.
        XmlError: If parsing fails.

    Example:
        >>> xml_file_to_json("data.xml")
        '{"root": {"item": "value"}}'
    """
    content = file_get_contents(filepath)
    parsed = parse_xml(content)
    return json.dumps(parsed)
