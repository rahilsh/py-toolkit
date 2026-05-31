from http.server import HTTPServer

from py_toolkit.server.server import ThreadingSimpleServer


class TestServer:
    def test_threading_simple_server_is_http_server(self):
        assert issubclass(ThreadingSimpleServer, HTTPServer)

    def test_server_has_reuse_address(self):
        assert ThreadingSimpleServer.allow_reuse_address is True

    def test_server_uses_daemon_threads(self):
        assert ThreadingSimpleServer.daemon_threads is True
