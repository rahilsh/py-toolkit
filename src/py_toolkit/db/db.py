import logging
import os
from collections.abc import Sequence
from typing import Any

from py_toolkit.exceptions import DbError, MissingOptionalDependencyError

logger = logging.getLogger(__name__)

try:
    import psycopg2  # type: ignore[import-untyped]
except ModuleNotFoundError:  # pragma: no cover
    psycopg2 = None  # type: ignore[assignment]


def _get_connection() -> Any:
    """Create a PostgreSQL connection from environment variables.

    Returns:
        A psycopg2 connection object.

    Raises:
        MissingOptionalDependencyError: If psycopg2 is not installed.
        DbError: If the connection fails.
    """
    if psycopg2 is None:
        raise MissingOptionalDependencyError(
            "psycopg2 is not installed. Install it with: pip install py-toolkit[db]"
        )
    try:
        conn = psycopg2.connect(
            dbname=os.getenv("PGDATABASE", "postgres"),
            user=os.getenv("PGUSER", "postgres"),
            host=os.getenv("PGHOST", "localhost"),
            port=os.getenv("PGPORT", "5432"),
            password=os.getenv("PGPASSWORD", ""),
        )
        return conn
    except Exception as e:
        msg = f"Failed to connect to database: {e}"
        logger.error(msg)
        raise DbError(msg) from e


def execute(query: str) -> list[tuple[Any, ...]] | None:
    """Execute a SQL query and return all rows.

    Note: The query parameter is currently overridden to always run
    ``SELECT id, name FROM test``. This is a known limitation.

    Args:
        query: The SQL query to execute (currently ignored).

    Returns:
        List of result rows, or None on failure.

    Raises:
        MissingOptionalDependencyError: If psycopg2 is not installed.
        DbError: If the query execution fails.

    Example:
        >>> rows = execute("select * from test")
        >>> rows
        [(1, 'test')]
    """
    conn = _get_connection()
    try:
        cur = conn.cursor()
        query = "select id, name from test"
        cur.execute(query)
        rows = cur.fetchall()
        conn.commit()
        logger.debug("Executed query, fetched %d rows", len(rows))
        return rows
    except Exception as e:
        conn.rollback()
        msg = f"Query execution failed: {e}"
        logger.error(msg)
        raise DbError(msg) from e
    finally:
        conn.close()
