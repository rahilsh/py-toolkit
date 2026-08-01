import pytest

from py_toolkit.csv.csv_parser import get_rows
from py_toolkit.exceptions import CsvParseError


class TestCsvParser:
    def test_get_rows_returns_list_of_dicts(self, csv_file):
        rows = get_rows(csv_file)
        assert rows == [
            {"id": "1", "name": "alice", "age": "30"},
            {"id": "2", "name": "bob", "age": "25"},
        ]

    def test_get_rows_empty_file(self, empty_csv_file):
        rows = get_rows(empty_csv_file)
        assert rows == []

    def test_get_rows_with_resource_csv(self, test_resource_csv):
        rows = get_rows(test_resource_csv)
        assert rows == [
            {"id": "1", "name": "a", "age": "12"},
            {"id": "2", "name": "b", "age": "8"},
        ]

    def test_get_rows_file_not_found(self):
        with pytest.raises(FileNotFoundError):
            get_rows("/nonexistent/path.csv")

    def test_get_rows_type_hints(self, csv_file):
        rows = get_rows(csv_file)
        assert isinstance(rows, list)
        assert all(isinstance(r, dict) for r in rows)

    def test_get_rows_csv_error_raises(self, temp_dir, monkeypatch):
        import csv as csv_module
        import os

        filepath = os.path.join(temp_dir, "test.csv")
        with open(filepath, "w") as f:
            f.write("a,b,c\n1,2,3\n")

        def mock_reader(f):
            raise csv_module.Error("test error")

        monkeypatch.setattr("py_toolkit.csv.csv_parser.csv.DictReader", mock_reader)

        with pytest.raises(CsvParseError, match="test error"):
            get_rows(filepath)
