import json
import logging

from py_toolkit.utils.request_util import request

if __name__ == '__main__':  # pragma: no cover
    users = json.load(open("/Users/rahil.r/Documents/zendesk/corpID_not_populated.json"))
    new_users = {"users": []}
    count = 0
    for user in users["results"]:
        count = count + 1
        try:
            email = user["email"]
            phone = user["phone"]
            new_user = {"email": email, "phone": phone}
            new_users["users"].append(new_user)
            print("===== Processing user no: {}, email: {}, phone: {} =====".format(count, email, phone))
            if email is None and phone is None:
                print("both phone,email not present. User ID: {}".format(user["id"]))
                continue
            if email is None:
                print("Email not present. User ID: {}".format(user["id"]))
                phone = str(phone).replace("+", "%2B")
                if len(phone) == 10:
                    phone = "%2B91" + phone
                if len(phone) < 10:
                    print("invalid phone number: {}. UserID: {}".format(phone, user["id"]))
                    continue
                querystring = {
                    "token": ""}
                url = "https://localhost/getProfileByMobile?mobileNumber=" + phone
                response_text, status_code = request(method="GET", url=url, params=querystring)
                print("Response: {}".format(response_text))
                if status_code == 200 and "corpID" in json.loads(response_text)["attrs"]:
                    print("corpID present !")
                else:
                    print("CorpID not present !")
                continue
            if phone is None:
                print("phone not present. User ID: {}".format(user["id"]))
                querystring = {"email": email,
                               "token": ""}
                url = "https://localhost/getProfileByEmail"
                response_text, status_code = request(method="GET", url=url, params=querystring)
                print("Response: {}".format(response_text))
                if status_code == 200 and "corpID" in json.loads(response_text)["attrs"]:
                    print("corpID present !")
                else:
                    print("CorpID not present !")
                continue
        except Exception as e:
            logging.exception("Error while processing user: {}".format(user))
            print("Error: {}".format(str(e)))
    print(json.dumps(new_users))
