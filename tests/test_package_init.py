from py_toolkit import __all__, __version__, exceptions


class TestPackageInit:
    def test_version_is_string(self):
        assert isinstance(__version__, str)
        assert len(__version__) > 0

    def test_all_exports_are_strings(self):
        assert all(isinstance(x, str) for x in __all__)

    def test_all_exports_exist(self):
        for name in __all__:
            if name == "__version__":
                continue
            assert hasattr(exceptions, name), f"{name} not found in exceptions"
