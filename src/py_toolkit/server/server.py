#!/usr/bin/env python3
"""Multithreaded HTTP file server.

Usage:
    python -m py_toolkit.server.server [port] [/path/to/share]
"""

import logging
import os
import sys
from http.server import HTTPServer, SimpleHTTPRequestHandler
from socketserver import ThreadingMixIn

logger = logging.getLogger(__name__)


class ThreadingSimpleServer(ThreadingMixIn, HTTPServer):
    """An HTTP server that handles each request in a separate thread.

    Combines :class:`socketserver.ThreadingMixIn` with
    :class:`http.server.HTTPServer` for concurrent request handling.

    Example:
        >>> server = ThreadingSimpleServer(('', 8000), SimpleHTTPRequestHandler)
        >>> server.handle_request()
    """

    allow_reuse_address = True
    daemon_threads = True
