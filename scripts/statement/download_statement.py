#!/usr/bin/env python3
"""Bulk-download bills for users from a CSV of user-card pairs."""

import csv
import io
import json
import logging
import os
from urllib.request import urlopen

from py_toolkit.pdf.pdf_to_image import convert_pdf_to_img
from py_toolkit.utils.folder_util import delete_dir, make_dir_from_path
from py_toolkit.utils.request_util import request
from py_toolkit.utils.unicode_util import to_unicode

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

QUARTER_FOLDER = os.getenv("QUARTER_FOLDER", "/tmp/folder/oct_dec/")
PROGRAM_TYPE = os.getenv("PROGRAM_TYPE", "asset")
LIST_OF_USER_CARDS = os.getenv("CSV_INPUT", os.path.join(QUARTER_FOLDER, f"{PROGRAM_TYPE}.csv"))
PROGRAM_FOLDER_PATH = os.getenv("OUTPUT_DIR", os.path.join(QUARTER_FOLDER, f"{PROGRAM_TYPE}/"))
API_BASE_URL = os.getenv("BILLS_API_URL", "https://localhost")
TOKEN = os.getenv("API_TOKEN", "")
UPLOADED_AT_START = os.getenv("DATE_FROM", "20180930")
UPLOADED_AT_END = os.getenv("DATE_TO", "20190101")


def process_bill(user_id: str, path: str, bill: dict) -> None:
    unique_key = bill["attrs"].get("billNumber", "") or bill["claimId"]
    unique_key = unique_key.replace("/", "_")
    logger.info("Processing bill: %s", unique_key)

    bills_folder = os.path.join(path, "bills", unique_key)
    make_dir_from_path(bills_folder)
    process_bill_urls(bill, bills_folder, unique_key, user_id)


def process_bill_urls(bill: dict, folder: str, key: str, user_id: str) -> None:
    for idx, bill_url in enumerate(bill["billUrls"], start=1):
        actual_bill = urlopen(bill_url)
        ct = actual_bill.headers["content-type"]
        ext = ".jpg"
        if ct == "application/pdf":
            ext = ".pdf"
        elif ct == "image/png":
            ext = ".png"
        elif ct != "image/jpeg":
            logger.warning("Unexpected type: user=%s bill=%s type=%s", user_id, key, ct)

        filepath = os.path.join(folder, f"{key}_{idx}{ext}")
        with open(filepath, "wb") as f:
            f.write(actual_bill.read())

        if ext == ".pdf":
            convert_pdf_to_img(filepath, folder + "/", f"{key}_{idx}")


def process_user_bills(bills: str, status: int, user_id: str) -> None:
    if status != 200:
        logger.warning("Non-200 response (%d) for user %s", status, user_id)
        return

    path = os.path.join(PROGRAM_FOLDER_PATH, str(user_id))
    delete_dir(path)
    make_dir_from_path(path)

    json_path = os.path.join(path, f"{user_id}.json")
    with io.open(json_path, "w", encoding="utf-8") as f:
        f.write(to_unicode(bills))

    bills_data = json.loads(bills)
    if not bills_data.get("bills"):
        logger.info("No bills found for user %s", user_id)
    for bill in bills_data["bills"]:
        process_bill(str(user_id), path, bill)


def process_user_cards(user_id: str, card_id: str) -> None:
    try:
        logger.info("Processing user: %s", user_id)
        url = (
            f"{API_BASE_URL}/userBills?token={TOKEN}"
            f"&userID={user_id}&count=100&cardID={card_id}"
            f"&dateRange.fromDateYYYYmmDD={UPLOADED_AT_START}"
            f"&dateRange.toDateYYYYmmDD={UPLOADED_AT_END}"
        )
        bills, status = request(method="GET", url=url)
        process_user_bills(bills, status, user_id)
    except Exception:
        logger.exception("Error processing user %s", user_id)


def process_users_cards() -> None:
    with open(LIST_OF_USER_CARDS) as csvfile:
        for row in csv.DictReader(csvfile):
            process_user_cards(row["userid"], row["cardid"])


def main() -> None:
    process_users_cards()
    logger.info("Done !!!")


if __name__ == "__main__":
    main()
