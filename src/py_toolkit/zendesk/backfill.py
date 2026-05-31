import json
import logging
import os

import requests

from py_toolkit.exceptions import RequestError

logger = logging.getLogger(__name__)


def stop_deployment() -> None:
    """Exit the process with a non-zero status code."""
    logger.error("Exiting due to deployment failure")
    raise SystemExit(1)


def request(
    method: str,
    url: str,
    headers: dict[str, str] | None = None,
    params: dict[str, str] | None = None,
    data: str | None = None,
) -> tuple[str, int]:
    """Make an HTTP request for Zendesk API operations.

    Args:
        method: HTTP method.
        url: Request URL.
        headers: Optional HTTP headers.
        params: Optional query parameters.
        data: Optional request body string.

    Returns:
        Tuple of ``(response_text, status_code)``.

    Raises:
        SystemExit: If the request fails.
    """
    logger.info("Making API call: %s %s", method, url)
    response: requests.Response | None = None
    try:
        response = requests.request(method, url, headers=headers, params=params, data=data, timeout=30)
        response_text = response.text
        response_status = response.status_code
        return response_text, response_status
    except requests.RequestException as e:
        data_str = data.encode("utf-8") if data else None
        logger.exception(
            "Request failed: method=%s url=%s data=%s",
            method,
            url,
            data_str,
        )
        stop_deployment()
    finally:
        if response is not None:
            response.close()
    return "", 0  # pragma: no cover


def main() -> None:  # pragma: no cover
    """Run the Zendesk user backfill process.

    Reads configuration from environment variables:
        - ``ZENDESK_DOMAIN``: Zendesk subdomain (default: ``host``)
        - ``ZENDESK_TOKEN``: Base64-encoded API token
        - ``UPDATE_USER_API``: Internal API URL for updating users
    """
    zendesk_domain = os.getenv("ZENDESK_DOMAIN", "host")
    zendesk_token = os.getenv("ZENDESK_TOKEN", "")
    update_user_api = os.getenv("UPDATE_USER_API", "https://localhost/zen/updateUser")

    max_page_no = 5000
    page_no = 1

    while True:
        logger.info("Processing page %d", page_no)
        url = f"https://{zendesk_domain}.zendesk.com:443/api/v2/search.json"
        querystring = {"page": str(page_no), "query": "iscorpuser:false type:user"}
        headers = {
            "Authorization": f"Basic {zendesk_token}",
        }

        try:
            response_text, response_status = request(
                method="GET", url=url, headers=headers, params=querystring
            )

            if response_status != 200:
                logger.warning("Response: %s", response_text)
            elif response_status == 200:
                logger.info("Users in page: %d", len(json.loads(response_text)["results"]))

            if response_status == 422 or len(json.loads(response_text)["results"]) == 0:
                logger.info("No more pages: %s", response_text)
                break

            for idx, user in enumerate(json.loads(response_text)["results"], start=1):
                logger.info(
                    "Processing user %d (page %d): email=%s phone=%s",
                    idx,
                    page_no,
                    user.get("email"),
                    user.get("phone"),
                )
                if user["email"] is None:
                    logger.info("Skipping user %s — no email", user["id"])
                    continue

                update_headers = {"Content-Type": "application/json"}
                update_data = json.dumps({"phone": user["phone"], "emailID": user["email"]})
                resp_text, resp_status = request(
                    method="POST",
                    url=update_user_api,
                    headers=update_headers,
                    data=update_data,
                )
                if resp_status != 200:
                    logger.warning(
                        "Update failed: status=%d response=%s",
                        resp_status,
                        resp_text,
                    )

            page_no += 1

        except Exception:
            logger.exception("Error occurred. Will retry in 10 seconds")
            import time
            time.sleep(10)

        if page_no > max_page_no:
            break


if __name__ == "__main__":  # pragma: no cover
    main()
