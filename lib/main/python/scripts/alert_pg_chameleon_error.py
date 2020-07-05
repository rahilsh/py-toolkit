import datetime
import json

from lib.main.python.utils.bash_util import run_bash_command
from lib.main.python.utils.request_util import request

print("Running at: " + str(datetime.datetime.now()))
f = open("/Users/rahil.r/code/bitbucket/python/python-test/lib/main/resources/attempt.txt", "r")
if f.mode == 'r' and "1" not in f.read():
    output = run_bash_command(
        "source /Users/rahil.r/Documents/python/venv/bin/activate && chameleon show_status --source mysql --config default")
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
