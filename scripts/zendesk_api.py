#!/usr/bin/env python3
"""Test the Zendesk API by fetching a ticket."""

import json
import logging
import os

import requests

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

ZENDESK_DOMAIN = os.getenv("ZENDESK_DOMAIN", "subdomain")
ZENDESK_TOKEN = os.getenv("ZENDESK_TOKEN", "<token>")
TICKET_ID = os.getenv("TICKET_ID", "388717")


def main() -> None:
    url = f"https://{ZENDESK_DOMAIN}.zendesk.com/api/v2/requests/{TICKET_ID}.json"
    headers = {"Authorization": f"Basic {ZENDESK_TOKEN}"}

    response = requests.request("GET", url, headers=headers, timeout=30)
    data = json.loads(response.text.encode("UTF-8"))
    logger.info("Ticket: %s", json.dumps(data.get("request"), indent=2))


if __name__ == "__main__":
    main()
