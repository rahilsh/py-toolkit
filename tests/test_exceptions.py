from py_toolkit.exceptions import (
    CsvParseError,
    DbError,
    MissingOptionalDependencyError,
    PdfError,
    RequestError,
    ToolkitError,
    XmlError,
)


class TestExceptions:
    def test_toolkit_error_is_base(self):
        assert issubclass(CsvParseError, ToolkitError)
        assert issubclass(RequestError, ToolkitError)
        assert issubclass(DbError, ToolkitError)
        assert issubclass(PdfError, ToolkitError)
        assert issubclass(XmlError, ToolkitError)
        assert issubclass(MissingOptionalDependencyError, ToolkitError)

    def test_missing_optional_is_also_import_error(self):
        assert issubclass(MissingOptionalDependencyError, ImportError)

    def test_toolkit_error_is_exception(self):
        assert issubclass(ToolkitError, Exception)

    def test_can_raise_and_catch_toolkit_error(self):
        try:
            raise CsvParseError("bad csv")
        except ToolkitError as e:
            assert str(e) == "bad csv"

    def test_error_message_preserved(self):
        msg = "something went wrong"
        try:
            raise RequestError(msg)
        except ToolkitError as e:
            assert str(e) == msg
