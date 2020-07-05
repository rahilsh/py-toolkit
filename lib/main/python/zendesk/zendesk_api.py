import json

import requests

url = "https://subdomain.zendesk.com/api/v2/requests/388717.json"

headers = {
    'Authorization': "Basic cmFoaWxyQHpldGEudGVjaDpaZXRhWmVuZGVza0AxNDUw",
    'Cache-Control': "no-cache",
    'Postman-Token': "dc5f0365-af80-404f-b4c2-e5fbe1f907cb"
}

response = requests.request("GET", url, headers=headers)

print(json.loads(response.text.encode("UTF-8"))["request"])
