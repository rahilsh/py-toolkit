import datetime
import json
import subprocess

import requests


def request(method, url, headers=None, params=None, data=None):
    response = None
    try:
        response = requests.request(method, url, headers=headers, params=params, data=data)
        response_text = response.text
        response_status = response.status_code
        return response_text, response_status
    except Exception as e:
        print("Error while making API call to jasper.Method: {}, URL: {}, headers: {}, params: {}, data: {}".format(
            method, url, headers, params, data))
        print("Error: {}".format(str(e)))
    finally:
        if response is not None:
            response.close()


def run_bash_command(command):
    print("Running command: {} \n".format(command))
    process = subprocess.Popen(command, shell=True, universal_newlines=True, stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE)
    output, error = process.communicate()
    print("Output: {}".format(str(output)))
    if process.returncode != 0:
        print("error: {}".format(str(error)))
    return str(output)


print("Running at: " + str(datetime.datetime.now()))
f = open("attempt.txt", "r")
if f.mode == 'r' and "1" not in f.read():
    output = run_bash_command(
        "source /Users/rahil.r/Documents/python/venv/bin/activate && chameleon show_status --source mysql --config default")
    if "error" in output or "initialised" in output:
        post_body = {
            'text': output
        }
        print("PostBody: " + str(json.dumps(post_body)))

        response, status = request(method='post',
                                   url='https://api.flock.com/hooks/sendMessage/e886cfae-9041-4e29-8ad1-fc31edc0dde6',
                                   data=json.dumps(post_body))
        print(response)
        f = open("attempt.txt", "w+")
        f.write("1")
        f.close()
    else:
        print(output)
else:
    print("Attempt is 1 hence ignoring")
