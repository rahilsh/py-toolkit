import pytest

from py_toolkit.zendesk.backfill import stop_deployment, request


class TestBackfill:
    def test_stop_deployment_exits(self):
        with pytest.raises(SystemExit):
            stop_deployment()

    def test_request_success(self, requests_mock):
        requests_mock.get("https://example.com/api", text='{"ok": true}', status_code=200)
        text, status = request("GET", "https://example.com/api")
        assert status == 200
        assert text == '{"ok": true}'

    def test_request_with_headers(self, requests_mock):
        requests_mock.post("https://example.com/submit", text="created", status_code=201)
        text, status = request("POST", "https://example.com/submit", data="payload")
        assert status == 201
        assert text == "created"

    def test_request_network_error_exits(self):
        with pytest.raises(SystemExit):
            request("GET", "https://nonexistent.invalid")
