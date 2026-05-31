#!/usr/bin/env python3
"""Validate Zendesk users by checking corpID via mobile or email lookup."""

import json
import logging
import os

from py_toolkit.utils.request_util import request

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

USERS_JSON = os.getenv("USERS_JSON", "/tmp/corpID_not_populated.json")
TOKEN = os.getenv("API_TOKEN", "")
API_BASE = os.getenv("PROFILE_API_URL", "https://localhost")


def main() -> None:
    with open(USERS_JSON) as f:
        users = json.load(f)

    new_users = {"users": []}

    for count, user in enumerate(users["results"], start=1):
        email = user.get("email")
        phone = user.get("phone")
        new_users["users"].append({"email": email, "phone": phone})

        logger.info("Processing user %d: email=%s phone=%s", count, email, phone)

        if email is None and phone is None:
            logger.warning("No email or phone for user %s", user["id"])
            continue

        if email is None:
            _check_by_phone(phone, user["id"])
        elif phone is None:
            _check_by_email(email, user["id"])

    print(json.dumps(new_users, indent=2))


def _check_by_phone(phone: str, user_id: str) -> None:
    phone_str = str(phone).replace("+", "%2B")
    if len(phone_str) == 12:
        phone_str = "%2B91" + phone_str[2:]
    if len(phone_str) < 10:
        logger.warning("Invalid phone for user %s: %s", user_id, phone_str)
        return

    qs = {"token": TOKEN}
    url = f"{API_BASE}/getProfileByMobile?mobileNumber={phone_str}"
    resp_text, status = request(method="GET", url=url, params=qs)
    logger.info("Response: %s", resp_text)

    if status == 200 and "corpID" in json.loads(resp_text).get("attrs", {}):
        logger.info("corpID present for user %s", user_id)
    else:
        logger.info("corpID NOT present for user %s", user_id)


def _check_by_email(email: str, user_id: str) -> None:
    qs = {"email": email, "token": TOKEN}
    url = f"{API_BASE}/getProfileByEmail"
    resp_text, status = request(method="GET", url=url, params=qs)
    logger.info("Response: %s", resp_text)

    if status == 200 and "corpID" in json.loads(resp_text).get("attrs", {}):
        logger.info("corpID present for user %s", user_id)
    else:
        logger.info("corpID NOT present for user %s", user_id)


if __name__ == "__main__":
    main()
