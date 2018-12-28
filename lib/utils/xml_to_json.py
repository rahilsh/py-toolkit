import json
import xmltodict


def file_get_contents(filename):
    with open(filename) as f:
        return f.read()


contents = file_get_contents('/Users/rahil.r/work/jasper/jasper-reports/reports/auto_deployment/report_with_one_integer_param.jrxml')
json_dumps = xmltodict.parse(contents)
parameter = json_dumps['jasperReport']['parameter']
print isinstance(parameter, dict)
print isinstance(parameter, list)
print json.dumps(parameter)
