from py_toolkit.utils.unicode_util import to_unicode


class TestUnicodeUtil:
    def test_to_unicode_is_callable(self):
        assert callable(to_unicode)

    def test_to_unicode_returns_str(self):
        result = to_unicode("hello")
        assert isinstance(result, str)
        assert result == "hello"

    def test_to_unicode_with_unicode_chars(self):
        result = to_unicode("héllo wörld")
        assert isinstance(result, str)
        assert result == "héllo wörld"

    def test_to_unicode_with_empty_string(self):
        result = to_unicode("")
        assert isinstance(result, str)
        assert result == ""

    def test_to_unicode_with_bytes_input(self):
        result = to_unicode(b"hello")
        assert isinstance(result, str)
        assert result == "b'hello'" or result == "hello"
