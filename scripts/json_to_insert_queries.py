#!/usr/bin/env python3
"""Generate SQL INSERT statements from sample employee data."""

import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

employees = (
    {"id": "1", "name": "a"},
    {"id": "2", "name": "b"},
)


def main() -> None:
    for employee in employees:
        sql = f"insert into employee (id, name) values ('{employee['id']}','{employee['name']}');"
        logger.info(sql)


if __name__ == "__main__":
    main()
