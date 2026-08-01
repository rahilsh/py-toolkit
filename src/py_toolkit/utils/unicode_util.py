"""Python 2/3 compatibility shim for unicode.

Provides a *to_unicode* function that works in both Python 2 and Python 3.
In Python 3 it is simply the built-in ``str`` type.
"""

try:
    to_unicode = unicode  # type: ignore[name-defined]  # noqa: F821
except NameError:
    to_unicode = str
