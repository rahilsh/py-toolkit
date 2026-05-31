from py_toolkit.server.server import ThreadingSimpleServer


class TestServer:
    def test_threading_simple_server_is_http_server(self):
        from http.server import HTTPServer
        assert issubclass(ThreadingSimpleServer, HTTPServer)
