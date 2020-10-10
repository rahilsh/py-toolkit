import json

import requests

url = "https://subdomain.zendesk.com/api/v2/requests/388717.json"

headers = {
    'Authorization': "Basic <token>"
}

response = requests.request("GET", url, headers=headers)

print(json.loads(response.text.encode("UTF-8"))["request"])
