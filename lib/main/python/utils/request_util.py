import requests


def request(method, url, headers=None, params=None, data=None):
    response = None
    try:
        response = requests.request(method, url, headers=headers, params=params, data=data)
        response_text = response.text
        response_status = response.status_code
        return response_text, response_status
    except Exception as e:
        print("Error while making API call to Method: {}, URL: {}, headers: {}, params: {}, data: {}".format(
            method, url, headers, params, data))
        print("Error: {}".format(str(e)))
    finally:
        if response is not None:
            response.close()
