import json

try:
    import xmltodict
except ModuleNotFoundError:
    xmltodict = None


def file_get_contents(filename):
    with open(filename) as f:
        return f.read()


def parse_xml(xml_content):
    if xmltodict is None:
        raise ImportError("xmltodict is not installed. Install it with: pip install py-toolkit[xml]")
    parsed = xmltodict.parse(xml_content)
    return parsed


if __name__ == '__main__':  # pragma: no cover
    contents = file_get_contents('/Users/rahil.shaikh/code/bitbucket/python/python-test/lib/main/resources/test.xml')
    json_dumps = xmltodict.parse(contents)
    parameter = json_dumps['test']['a']
    print(isinstance(parameter, dict))
    print(isinstance(parameter, list))
    print(json.dumps(parameter))
