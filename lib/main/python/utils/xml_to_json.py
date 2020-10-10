import json
import xmltodict


def file_get_contents(filename):
    with open(filename) as f:
        return f.read()


contents = file_get_contents('/Users/rahil.shaikh/code/bitbucket/python/python-test/lib/main/resources/test.xml')
json_dumps = xmltodict.parse(contents)
parameter = json_dumps['test']['a']
print(isinstance(parameter, dict))
print(isinstance(parameter, list))
print(json.dumps(parameter))
