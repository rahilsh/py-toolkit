#!/usr/bin/env python3
"""Download bills from an API using claim IDs."""

import json
import logging
import os
from urllib.request import urlopen

from py_toolkit.utils.request_util import request

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

API_BASE_URL = os.getenv("BILLS_API_URL", "https://localhost:8080")
TOKEN = os.getenv("API_TOKEN", "")
CLAIM_IDS = os.getenv("CLAIM_IDS", "9dc2ed23-3ca9-4f36-b8b5-924cfc45f07d_1544805742102-o3V4").split(",")
OUTPUT_DIR = os.getenv("OUTPUT_DIR", "/tmp/bills")


def get_bill(claim_id: str) -> None:
    url = f"{API_BASE_URL}/getBill?token={TOKEN}&claimID={claim_id}"
    bill, status_code = request(method="GET", url=url)
    process_bill(json.loads(bill))


def process_bill(bill: dict) -> None:
    count = 1
    for bill_url in bill["billUrls"]:
        actual_bill = urlopen(bill_url)
        ext = _get_extension(actual_bill.headers["content-type"])
        if len(bill["billUrls"]) == 1:
            count_suffix = ""
        else:
            count_suffix = f"_{count}"

        filename = os.path.join(OUTPUT_DIR, f"{bill['claimId'].split('_')[1]}{count_suffix}{ext}")
        with open(filename, "wb") as output:
            output.write(actual_bill.read())
        logger.info("Downloaded: %s", filename)
        count += 1


def _get_extension(content_type: str) -> str:
    mapping = {
        "application/pdf": ".pdf",
        "image/png": ".png",
        "image/jpeg": ".jpg",
    }
    return mapping.get(content_type, ".jpg")


def main() -> None:
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    for claim_id in CLAIM_IDS:
        logger.info("Processing: %s", claim_id)
        get_bill(claim_id)
    logger.info("Done !!!")


if __name__ == "__main__":
    main()
