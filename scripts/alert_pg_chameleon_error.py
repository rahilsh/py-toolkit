#!/usr/bin/env python3
"""Alert on pg_chameleon replication errors by posting to a Slack webhook."""

import datetime
import json
import logging
import os
import subprocess

from py_toolkit.utils.request_util import request

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

ATTEMPT_FILE = os.getenv("ATTEMPT_FILE", "/tmp/attempt_pg_chameleon.txt")
SLACK_WEBHOOK_URL = os.getenv("SLACK_WEBHOOK_URL", "")


def main() -> None:
    logger.info("Running at: %s", datetime.datetime.now())

    try:
        with open(ATTEMPT_FILE) as f:
            if "1" in f.read():
                logger.info("Attempt flag is 1 — skipping")
                return
    except FileNotFoundError:
        pass

    output = subprocess.check_output(
        "chameleon show_status --source mysql --config default",
        shell=True,
        text=True,
        stderr=subprocess.STDOUT,
    )

    if "error" in output.lower() or "initialised" in output.lower():
        logger.warning("Replication issue detected:\n%s", output)

        if SLACK_WEBHOOK_URL:
            post_body = {"text": output}
            response, status = request(
                method="POST",
                url=SLACK_WEBHOOK_URL,
                data=json.dumps(post_body),
            )
            logger.info("Slack response (status %d): %s", status, response)
        else:
            logger.warning("SLACK_WEBHOOK_URL not set — would post:\n%s", output)

        with open(ATTEMPT_FILE, "w") as f:
            f.write("1")
    else:
        logger.info("Status OK:\n%s", output)


if __name__ == "__main__":
    main()
