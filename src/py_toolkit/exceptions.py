class ToolkitError(Exception):
    """Base exception for all py-toolkit errors."""


class CsvParseError(ToolkitError):
    """Raised when CSV parsing fails."""


class RequestError(ToolkitError):
    """Raised when an HTTP request fails."""


class DbError(ToolkitError):
    """Raised when a database operation fails."""


class PdfError(ToolkitError):
    """Raised when a PDF operation fails."""


class XmlError(ToolkitError):
    """Raised when an XML operation fails."""


class GitError(ToolkitError):
    """Raised when a git or GitHub operation fails."""


class MissingOptionalDependencyError(ToolkitError, ImportError):
    """Raised when an optional dependency is not installed."""
