from importlib.metadata import version, PackageNotFoundError

try:
    __version__ = version("py-toolkit")
except PackageNotFoundError:  # pragma: no cover
    __version__ = "0.0.0"

from py_toolkit.exceptions import (
    ToolkitError,
    CsvParseError,
    RequestError,
    DbError,
    PdfError,
    XmlError,
    MissingOptionalDependencyError,
)

__all__ = [
    "__version__",
    "ToolkitError",
    "CsvParseError",
    "RequestError",
    "DbError",
    "PdfError",
    "XmlError",
    "MissingOptionalDependencyError",
]
