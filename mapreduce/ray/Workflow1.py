import requests
import json
import time
import subprocess
import threading
from flask import Flask

app = Flask(__name__)

mapper_name = "wc-mapper"
reducer_name = "wc-reducer"
mapper_num = 5
reducer_num = 5
headers = {
        "Content-Type": "application/json",
        "accept": "application/json",
    }
mapurl = "http://10.244.0.150:8000/wc/map"
reduceurl = "http://10.244.0.150:8000/wc/reduce"



def post(url, data):
    text = requests.post(url, data=data, headers=headers).text


def workflow():
    start = time.time()


    threads = []
    for i in range(mapper_num):
        req = json.dumps({"input_name": "data-500m", "input_part": i, "reduce_num": reducer_num})
        t = threading.Thread(target=post, args=(mapurl, req))
        threads.append(t)

    for t in threads:
        t.start()

    for t in threads:
        t.join()

    mapper_end = time.time()


    threads = []
    for i in range(reducer_num):
        req = json.dumps({"input_name": "data-500m", "input_num": mapper_num, "reduce_part": i})
        t = threading.Thread(target=post, args=(reduceurl, req))
        threads.append(t)

    for t in threads:
        t.start()

    for t in threads:
        t.join()

    reducer_end = time.time()

    return "time: %d " % (reducer_end-start)




@app.route('/hi')
def index():
    res = workflow()
    # get_res_info(reducer_res)
    return {
        "msg": "success",
        "data": res
    }


if __name__ == "__main__":
    app.run()