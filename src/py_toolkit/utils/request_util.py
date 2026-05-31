import logging
from typing import Any

import requests

from py_toolkit.exceptions import RequestError

logger = logging.getLogger(__name__)


def request(
    method: str,
    url: str,
    headers: dict[str, str] | None = None,
    params: dict[str, str] | None = None,
    data: Any = None,
) -> tuple[str, int]:
    """Make an HTTP request and return the response text and status code.

    Args:
        method: HTTP method (GET, POST, PUT, DELETE, etc.).
        url: Request URL.
        headers: Optional HTTP headers.
        params: Optional URL query parameters.
        data: Optional request body data.

    Returns:
        Tuple of ``(response_text, status_code)``.

    Raises:
        RequestError: If the request fails due to a network error or non-2xx status.

    Example:
        >>> text, status = request("GET", "https://api.example.com/data")
        >>> status
        200
    """
    response: requests.Response | None = None
    try:
        response = requests.request(method, url, headers=headers, params=params, data=data, timeout=30)
        response_text = response.text
        response_status = response.status_code
        logger.debug("Request %s %s returned %d", method, url, response_status)
        return response_text, response_status
    except requests.RequestException as e:
        msg = f"Request {method} {url} failed: {e}"
        logger.error(msg)
        raise RequestError(msg) from e
    finally:
        if response is not None:
            response.close()
