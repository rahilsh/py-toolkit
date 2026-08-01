from importlib.metadata import PackageNotFoundError, version

try:
    __version__ = version("py-toolkit")
except PackageNotFoundError:  # pragma: no cover
    __version__ = "0.0.0"

from py_toolkit.exceptions import (
    CsvParseError,
    DbError,
    MissingOptionalDependencyError,
    PdfError,
    RequestError,
    ToolkitError,
    XmlError,
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
