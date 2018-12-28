import base64


def get_file_contents(filename):
    with open(filename) as f:
        return f.read()


report_design = get_file_contents('/Users/rahil.r/JaspersoftWorkspace/MyReports/ictest/test.jrxml')
encoded_report = base64.b64encode(report_design)

print encoded_report
