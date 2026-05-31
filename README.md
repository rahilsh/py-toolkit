# py-toolkit

Utility library to accelerate development with common helpers for CSV parsing, PDF conversion, HTTP requests, file/folder management, and more.

## Installation

```bash
pip install py-toolkit
```

With optional dependencies:

```bash
pip install py-toolkit[pdf]    # PDF support (pdf2image)
pip install py-toolkit[db]     # Database support (psycopg2-binary)
pip install py-toolkit[xml]    # XML support (xmltodict)
pip install py-toolkit[dev]    # Development tools (pytest, pytest-cov)
```

## Modules

| Module | Description |
|---|---|
| `py_toolkit.csv.csv_parser` | Parse CSV files into dictionaries |
| `py_toolkit.utils.folder_util` | Create and delete directories |
| `py_toolkit.utils.request_util` | HTTP request wrapper using `requests` |
| `py_toolkit.utils.unicode_util` | Python 2/3 unicode compatibility shim |
| `py_toolkit.utils.xml_to_json` | Convert XML files to JSON |
| `py_toolkit.pdf.pdf_to_image` | Convert PDF pages to JPEG images |
| `py_toolkit.db.db` | PostgreSQL database helpers |
| `py_toolkit.server.server` | Multithreaded HTTP file server |
| `py_toolkit.statement` | Bill/download statement processors |
| `py_toolkit.zendesk` | Zendesk API integration scripts |
| `py_toolkit.scripts` | Miscellaneous utility scripts |

## Usage

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

## Development

```bash
# Install development dependencies
pip install -e ".[dev]"

# Run tests with coverage
pytest --cov --cov-report=term-missing

# Run linter
ruff check src/
```

## Project Structure

```
src/
└── py_toolkit/
    ├── csv/         # CSV parsing
    ├── db/          # Database utilities
    ├── pdf/         # PDF conversion
    ├── scripts/     # Utility scripts
    ├── server/      # HTTP server
    ├── statement/   # Bill download processors
    ├── utils/       # Core utilities
    └── zendesk/     # Zendesk API integration
tests/
├── resources/       # Test fixtures
└── test_*.py        # Test files
```
