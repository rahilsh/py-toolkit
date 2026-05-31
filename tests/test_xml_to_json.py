from unittest import mock

import pytest

from py_toolkit.utils.xml_to_json import file_get_contents, parse_xml


class TestXmlToJson:
    def test_file_get_contents_returns_content(self, xml_file):
        content = file_get_contents(xml_file)
        assert "<?xml" in content
        assert "<test>" in content

    def test_file_get_contents_empty_file(self, temp_dir):
        import os
        filepath = os.path.join(temp_dir, "empty.txt")
        with open(filepath, "w") as f:
            f.write("")
        content = file_get_contents(filepath)
        assert content == ""

    def test_file_get_contents_file_not_found(self):
        with pytest.raises(FileNotFoundError):
            file_get_contents("/nonexistent/file.xml")

    def test_parse_xml_returns_dict(self, xml_file):
        content = file_get_contents(xml_file)
        result = parse_xml(content)
        assert isinstance(result, dict)

    def test_parse_xml_with_nested_elements(self):
        xml = "<root><item id='1'>value</item></root>"
        result = parse_xml(xml)
        assert result == {"root": {"item": {"@id": "1", "#text": "value"}}}

    def test_parse_xml_list_elements(self, xml_file):
        content = file_get_contents(xml_file)
        result = parse_xml(content)
        assert "test" in result
        assert isinstance(result["test"]["a"]["item"], list)

    def test_parse_xml_invalid_xml(self):
        with pytest.raises(Exception):
            parse_xml("<not><valid>xml")

    @mock.patch("py_toolkit.utils.xml_to_json.xmltodict", None)
    def test_parse_xml_raises_when_xmltodict_missing(self):
        with pytest.raises(ImportError, match="xmltodict"):
            parse_xml("<root/>")
