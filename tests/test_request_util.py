import pytest

from py_toolkit.exceptions import RequestError
from py_toolkit.utils.request_util import request


class TestRequestUtil:
    def test_request_get_success(self, requests_mock):
        requests_mock.get("https://example.com/api", text='{"ok": true}', status_code=200)
        text, status = request("GET", "https://example.com/api")
        assert status == 200
        assert text == '{"ok": true}'

    def test_request_get_not_found(self, requests_mock):
        requests_mock.get("https://example.com/404", text="Not Found", status_code=404)
        text, status = request("GET", "https://example.com/404")
        assert status == 404
        assert text == "Not Found"

    def test_request_post_with_data(self, requests_mock):
        requests_mock.post("https://example.com/submit", text="created", status_code=201)
        text, status = request("POST", "https://example.com/submit", data="payload")
        assert status == 201
        assert text == "created"

    def test_request_with_headers(self, requests_mock):
        requests_mock.get("https://example.com/auth", text="ok", status_code=200)
        text, status = request("GET", "https://example.com/auth", headers={"Authorization": "Bearer xyz"})
        assert status == 200

    def test_request_with_params(self, requests_mock):
        requests_mock.get("https://example.com/search", text="results", status_code=200)
        text, status = request("GET", "https://example.com/search", params={"q": "test"})
        assert status == 200

    def test_request_network_error_raises(self):
        with pytest.raises(RequestError):
            request("GET", "https://nonexistent.invalid")

    def test_request_connection_error_raises(self):
        with pytest.raises(RequestError):
            request("GET", "https://localhost:1")

    def test_request_response_closed_in_finally(self, requests_mock):
        requests_mock.get("https://example.com/close-test", text="ok", status_code=200)
        text, status = request("GET", "https://example.com/close-test")
        assert status == 200
        assert text == "ok"

    def test_request_returns_tuple(self, requests_mock):
        requests_mock.get("https://example.com/tuple", text="data", status_code=200)
        result = request("GET", "https://example.com/tuple")
        assert isinstance(result, tuple)
        assert len(result) == 2
