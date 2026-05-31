import os
import tempfile

import pytest


@pytest.fixture
def temp_dir():
    with tempfile.TemporaryDirectory() as tmpdir:
        yield tmpdir


@pytest.fixture
def csv_file(temp_dir):
    filepath = os.path.join(temp_dir, "test.csv")
    with open(filepath, "w") as f:
        f.write("id,name,age\n1,alice,30\n2,bob,25\n")
    return filepath


@pytest.fixture
def empty_csv_file(temp_dir):
    filepath = os.path.join(temp_dir, "empty.csv")
    with open(filepath, "w") as f:
        f.write("id,name,age\n")
    return filepath


@pytest.fixture
def test_resource_csv():
    return os.path.join(os.path.dirname(__file__), "resources", "employee.csv")


@pytest.fixture
def xml_file(temp_dir):
    filepath = os.path.join(temp_dir, "test.xml")
    with open(filepath, "w") as f:
        f.write('<?xml version="1.0"?><test><a><item>value1</item><item>value2</item></a></test>')
    return filepath
