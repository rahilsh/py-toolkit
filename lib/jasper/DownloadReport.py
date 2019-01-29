import requests

url = "http://c1b.aws.zeta.in:8080/jasperserver/rest_v2/reports/reports/prod/ReportCenter/prod/Corp_Benefits/FundingAccount/FundingAccountDeposits.csv"

querystring = {"j_username":"jasperadmin","j_password":"jasperadmin","fundingAccountIDs":"7022265865805583845","fundingAccountNames":"[Test]%20Test%20Today","endDate":"1529951399000","startDate":"1514745000000"}

payload = ""
headers = {
    'Content-Type': "text/csv",
    'cache-control': "no-cache",
    'Postman-Token': "6ff9ae4e-3ede-4940-a607-6fbe234ba48b"
    }

response = requests.request("GET", url, data=payload, headers=headers, params=querystring)

print(response.text)