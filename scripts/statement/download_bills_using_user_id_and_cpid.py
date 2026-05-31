#!/usr/bin/env python3
"""Download bills for users by user ID and card program ID."""

import csv
import json
import logging
import os
from urllib.request import urlopen

from py_toolkit.utils.folder_util import make_dir_from_path
from py_toolkit.utils.request_util import request

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

API_BASE_URL = os.getenv("BILLS_API_URL", "https://localhost")
TOKEN = os.getenv("API_TOKEN", "")
CSV_INPUT = os.getenv("CSV_INPUT", "/tmp/test.csv")
OUTPUT_BASE = os.getenv("OUTPUT_DIR", "/tmp/bills")


def get_bill(user_id: str, cardprogram_id: str) -> str:
    url = f"{API_BASE_URL}/userBills?token={TOKEN}&userID={user_id}&cardProgramID={cardprogram_id}"
    bills, _ = request(method="GET", url=url)
    return bills


def process_bill(bill: dict, folder_path: str) -> None:
    count = 1
    for bill_url in bill["billUrls"]:
        actual_bill = urlopen(bill_url)
        ext = ".jpg"
        ct = actual_bill.headers["content-type"]
        if ct == "application/pdf":
            ext = ".pdf"
        elif ct == "image/png":
            ext = ".png"
        elif ct != "image/jpeg":
            logger.warning("Unexpected content-type %s for bill %s", ct, bill["claimId"])

        filename = os.path.join(
            folder_path,
            f"{bill['claimId'].split('_')[1]}{'' if len(bill['billUrls']) == 1 else '_' + str(count)}{ext}",
        )
        with open(filename, "wb") as output:
            output.write(actual_bill.read())
        count += 1


def main() -> None:
    with open(CSV_INPUT) as csv_file:
        for row in csv.reader(csv_file):
            if len(row) < 3:
                continue
            user_id, email, cardprogram_id = row[0], row[1], row[2]
            logger.info("Processing: %s %s %s", user_id, email, cardprogram_id)

            bills = json.loads(get_bill(user_id, cardprogram_id))
            folder_path = os.path.join(OUTPUT_BASE, email)
            try:
                make_dir_from_path(folder_path)
            except Exception:
                logger.exception("Failed to create folder for user %s", user_id)

            for bill in bills.get("bills", []):
                process_bill(bill, folder_path)


if __name__ == "__main__":
    main()
