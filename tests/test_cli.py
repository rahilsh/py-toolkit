from py_toolkit import __version__
from py_toolkit.cli import build_parser


class TestCli:
    def test_parser_builds(self):
        parser = build_parser()
        assert parser is not None

    def test_version_in_help(self):
        parser = build_parser()
        assert "--version" in parser.format_help()

    def test_csv_subcommand(self):
        parser = build_parser()
        parsed = parser.parse_args(["csv", "test.csv"])
        assert parsed.command == "csv"
        assert parsed.file == "test.csv"

    def test_serve_subcommand(self):
        parser = build_parser()
        parsed = parser.parse_args(["serve", "--port", "8080", "--dir", "/tmp"])
        assert parsed.command == "serve"
        assert parsed.port == 8080
        assert parsed.dir == "/tmp"

    def test_xml2json_subcommand(self):
        parser = build_parser()
        parsed = parser.parse_args(["xml2json", "data.xml"])
        assert parsed.command == "xml2json"
        assert parsed.file == "data.xml"

    def test_verbose_flag(self):
        parser = build_parser()
        parsed = parser.parse_args(["-v", "csv", "f.csv"])
        assert parsed.verbose == 1

    def test_verbose_debug(self):
        parser = build_parser()
        parsed = parser.parse_args(["-vv", "csv", "f.csv"])
        assert parsed.verbose == 2

    def test_version_attr(self):
        assert isinstance(__version__, str)
        assert len(__version__) > 0

    def test_no_command_prints_help(self, capsys):
        from py_toolkit.cli import main

        try:
            main(["--help"])
        except SystemExit:
            pass
        captured = capsys.readouterr()
        assert "usage:" in captured.out or "usage:" in captured.err
