import pytest

from py_toolkit.csv.csv_parser import get_rows


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
