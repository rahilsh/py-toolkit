import datetime
import json
import subprocess

from py_toolkit.utils.request_util import request

if __name__ == '__main__':  # pragma: no cover
    print("Running at: " + str(datetime.datetime.now()))
    f = open("/Users/rahil.r/code/bitbucket/python/python-test/lib/main/resources/attempt.txt", "r")
    if f.mode == 'r' and "1" not in f.read():
        output = subprocess.check_output(
            "source /Users/rahil.r/Documents/python/venv/bin/activate && chameleon show_status --source mysql --config default",
            shell=True, text=True)
        if "error" in output or "initialised" in output:
            post_body = {
                'text': output
            }
            print("PostBody: " + str(json.dumps(post_body)))

            response, status = request(method='post',
                                       url='',
                                       data=json.dumps(post_body))
            print(response)
            f = open("/Users/rahil.r/code/bitbucket/python/python-test/lib/main/resources/attempt.txt", "w+")
            f.write("1")
            f.close()
        else:
            print(output)
    else:
        print("Attempt is 1 hence ignoring")
