from unittest import mock

import pytest

from py_toolkit.db.db import _get_connection, execute
from py_toolkit.exceptions import DbError, MissingOptionalDependencyError


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
    def test_execute_raises_on_connect_error(self, mock_psycopg2):
        mock_psycopg2.connect.side_effect = Exception("Connection refused")
        with pytest.raises(DbError, match="Connection refused"):
            execute("select * from test")

    @mock.patch("py_toolkit.db.db.psycopg2")
    def test_execute_raises_on_query_error(self, mock_psycopg2):
        mock_conn = mock_psycopg2.connect.return_value
        mock_cur = mock_conn.cursor.return_value
        mock_cur.execute.side_effect = Exception("Syntax error")
        with pytest.raises(DbError, match="Syntax error"):
            execute("select * from test")

    @mock.patch("py_toolkit.db.db.psycopg2", None)
    def test_execute_raises_when_psycopg2_missing(self):
        with pytest.raises(MissingOptionalDependencyError, match="psycopg2"):
            execute("select * from test")

    @mock.patch("py_toolkit.db.db.psycopg2")
    def test_get_connection_success(self, mock_psycopg2):
        conn = _get_connection()
        assert conn is mock_psycopg2.connect.return_value

    @mock.patch("py_toolkit.db.db.psycopg2")
    def test_get_connection_raises_on_failure(self, mock_psycopg2):
        mock_psycopg2.connect.side_effect = Exception("db down")
        with pytest.raises(DbError, match="db down"):
            _get_connection()

    @mock.patch("py_toolkit.db.db.psycopg2", None)
    def test_get_connection_raises_when_missing(self):
        with pytest.raises(MissingOptionalDependencyError, match="psycopg2"):
            _get_connection()
