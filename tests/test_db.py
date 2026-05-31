from unittest import mock

from py_toolkit.db.db import execute


class TestDb:
    @mock.patch("py_toolkit.db.db.psycopg2")
    def test_execute_returns_rows(self, mock_psycopg2):
        mock_conn = mock_psycopg2.connect.return_value
        mock_cur = mock_conn.cursor.return_value
        mock_cur.fetchall.return_value = [(1, "test")]
        result = execute("select * from test")
        assert result == [(1, "test")]
        mock_cur.execute.assert_called_once_with("select id, name from test")

    @mock.patch("py_toolkit.db.db.psycopg2")
    def test_execute_handles_error(self, mock_psycopg2):
        mock_psycopg2.connect.side_effect = Exception("Connection refused")
        result = execute("select * from test")
        assert result is None
