import json
import logging
import time

import requests


def stop_deployment():
    print("Exiting !!!")
    exit(1)


def request(method, url, headers=None, params=None, data=None):
    print("Making API call. Method: {}, URL: {}, headers: {}, params: {}".format(
        method, url, headers, params))
    response = None
    try:
        response = requests.request(method, url, headers=headers, params=params, data=data)
        response_text = response.text
        response_status = response.status_code
        return response_text, response_status
    except Exception as e:
        logging.exception("Error while making API call. Method: {}, URL: {}, headers: {}, params: {}, data: {}".format(
            method, url, headers, params, data.encode('utf-8')))
        print("Error: {}".format(str(e)))
        stop_deployment()
    finally:
        if response is not None:
            response.close()


def main():
    max_page_no = 5000
    page_no = 1
    while True:
        print("Processing page {}".format(page_no))
        url = "https://host.zendesk.com:443/api/v2/search.json"

        querystring = {"page": page_no, "query": "iscorpuser:false type:user"}

        headers = {
            'Authorization': "Basic cHJvZHVjdC1zdXBwb3J0QHpldGEudGVjaDp0dkskNFVTWmpkLio="
        }
        try:
            response_text, response_status = request(method="GET", url=url, headers=headers, params=querystring)
            if response_status != 200:
                print("Response: {}".format(response_text.encode('utf-8')))
            elif response_status == 200:
                print("No of users: {}".format(len(json.loads(response_text)["results"])))

            if response_status == 422 or len(json.loads(response_text)["results"]) == 0:
                print("No more pages: {}".format(response_text))
                break
            user_count = 1
            for user in json.loads(response_text)["results"]:
                print("Processing user no {},{}. Email: {}, phone: {}.".format(user_count, page_no, user["email"],
                                                                               user["phone"]))
                if user["email"] is None:
                    print("Ignoring user as email is none. userID: {}".format(user["id"]))
                    user_count = user_count + 1
                    continue
                url = "https://localhost/zen/updateUser"
                headers = {
                    'Content-Type': "application/json"
                }
                response_text, response_status = request(method="POST", url=url, headers=headers,
                                                         data=json.dumps(
                                                             {"phone": user["phone"], "emailID": user["email"]}))
                if response_status != 200:
                    print("response_text: {}. response_status: {}".format(response_text,
                                                                          str(response_status)))
                user_count = user_count + 1
            page_no = page_no + 1
        except Exception as e:
            logging.exception("Error occurred. Will try after 10 seconds !!!")
            print("Error: {}".format(str(e)))
            time.sleep(10)
        if page_no > max_page_no:
            break


if __name__ == '__main__':
    main()
