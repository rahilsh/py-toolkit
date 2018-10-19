import requests

count = 3317
headers = {
    'Accept': "application/json"
}
params = {"j_username": "jasperadmin", "j_password": "jasperadmin"}
while count < 3376:
    print
    "processing {}".format(count)
    response = requests.request("DELETE", "http://c1b.aws.zeta.in:8080/jasperserver/rest_v2/jobs/" + str(count),
                                headers=headers, params=params)
    print(response.status_code)
    print(response.text)
    count = count + 1
