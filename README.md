# py-toolkit

[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](https://opensource.org/licenses/MIT)
[![CI](https://github.com/rahilsh/py-toolkit/actions/workflows/python-app.yml/badge.svg)](https://github.com/rahilsh/py-toolkit/actions/workflows/python-app.yml)
[![Coverage](https://img.shields.io/badge/coverage-%3E85%25-brightgreen)](https://github.com/rahilsh/py-toolkit)
[![Ruff](https://img.shields.io/badge/code_style-ruff-000000.svg)](https://github.com/astral-sh/ruff)

Utility library to accelerate development with common helpers for CSV parsing, PDF conversion, HTTP requests, file/folder management, XML conversion, and more.

## Installation

```bash
pip install py-toolkit
```

With optional features:

```bash
pip install py-toolkit[pdf]     # PDF support (pdf2image)
pip install py-toolkit[db]      # Database support (psycopg2-binary)
pip install py-toolkit[xml]     # XML support (xmltodict)
pip install py-toolkit[dev]     # Development tools
```

## Quick Start

```python
from py_toolkit.csv.csv_parser import get_rows
from py_toolkit.utils.folder_util import make_dir_from_path, delete_dir
from py_toolkit.utils.request_util import request

# Parse a CSV file
rows = get_rows("data.csv")

# Create/delete directories
make_dir_from_path("/tmp/my_folder")
delete_dir("/tmp/my_folder")

# Make HTTP requests
response_text, status_code = request("GET", "https://api.example.com/data")
```

## CLI Usage

The package provides a ``py-toolkit`` command after installation:

```bash
py-toolkit --version
py-toolkit csv data.csv
py-toolkit xml2json data.xml
py-toolkit serve --port 8080 --dir /path/to/share
```

## Modules

### Core Utilities

| Module | Description |
|---|---|
| `py_toolkit.csv.csv_parser` | Parse CSV files into dictionaries |
| `py_toolkit.utils.folder_util` | Create and delete directories |
| `py_toolkit.utils.request_util` | HTTP request wrapper using `requests` |
| `py_toolkit.utils.unicode_util` | Python 2/3 unicode compatibility |
| `py_toolkit.utils.xml_to_json` | Convert XML to JSON |

### Optional Features

| Module | Requires | Description |
|---|---|---|
| `py_toolkit.db.db` | `[db]` | PostgreSQL database helpers |
| `py_toolkit.pdf.pdf_to_image` | `[pdf]` | Convert PDF pages to JPEG images |
| `py_toolkit.server.server` | — | Multithreaded HTTP file server |

## API Reference

### CSV

```python
from py_toolkit.csv.csv_parser import get_rows

rows = get_rows("file.csv")  # -> list[dict[str, str]]
```

### Folder Utilities

```python
from py_toolkit.utils.folder_util import make_dir_from_path, delete_dir

make_dir_from_path("/tmp/a/b/c")  # creates all parent dirs
delete_dir("/tmp/a")              # recursive delete, no error if missing
```

### HTTP Requests

```python
from py_toolkit.utils.request_util import request

text, status = request("GET", "https://api.example.com/data")
text, status = request("POST", "https://api.example.com/submit", data='{"key": "val"}')
```

### XML to JSON

```python
from py_toolkit.utils.xml_to_json import parse_xml, xml_file_to_json

data = parse_xml("<root><item>value</item></root>")
json_str = xml_file_to_json("data.xml")
```

### Database

```python
from py_toolkit.db.db import execute

rows = execute("SELECT * FROM users")
```

Configure via environment variables: ``PGDATABASE``, ``PGUSER``, ``PGHOST``, ``PGPORT``, ``PGPASSWORD``.

## Development

```bash
# Clone and install
git clone https://github.com/rahilsh/py-toolkit.git
cd py-toolkit
pip install -e ".[dev,db,xml]"

# Install pre-commit hooks
pre-commit install

# Run tests with coverage
pytest --cov --cov-report=term-missing

# Run linter
ruff check src/ tests/

# Check formatting
ruff format --check src/ tests/

# Run across all Python versions
tox
```

## Project Structure

```
src/
└── py_toolkit/
    ├── __init__.py       # Package version, exception exports
    ├── exceptions.py     # Custom exception hierarchy
    ├── cli.py            # CLI entry point
    ├── csv/              # CSV parsing
    ├── db/               # Database utilities
    ├── pdf/              # PDF conversion
    ├── server/           # HTTP server
    └── utils/            # Core utilities (folder, request, unicode, xml)
tests/
├── resources/            # Test fixtures
├── conftest.py           # Shared fixtures
└── test_*.py             # Test files
```

## Error Handling

All library functions raise specific exceptions from ``py_toolkit.exceptions``:

```python
from py_toolkit.exceptions import (
    ToolkitError,
    CsvParseError,
    RequestError,
    DbError,
    PdfError,
    XmlError,
    MissingOptionalDependencyError,
)
```

## Changelog

See [CHANGELOG.md](CHANGELOG.md) for a full history of notable changes.

## Contributing

Contributions are welcome! Please read the [contributing guide](CONTRIBUTING.md)
to get started, and note that this project is released under the
[Contributor Covenant Code of Conduct](CODE_OF_CONDUCT.md).

## Security

If you discover a security vulnerability, please follow the process described in
our [security policy](SECURITY.md). Do not open a public issue for security
reports.

## License

This project is licensed under the terms of the [MIT License](LICENSE).

