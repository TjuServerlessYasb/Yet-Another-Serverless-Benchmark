import requests
import threading

import json
import time
from flask import Flask

app = Flask(__name__)

headers = {
    "Content-Type": "application/json",
    "accept": "application/json",
    }

margin_balance_url = "http://10.244.0.158:8000/fi/marginBalance"

funcs = ["marketdata", "lastpx", "side", "trddate", "volume"]

urls = [f"http://10.244.0.158:8000/fi/{func}" for func in funcs]

req = {"body":{ "portfolioType":"S&P", "portfolio":"1234"}}


def post(url, data, l):
    res = requests.post(url, data=data, headers=headers).text
    print(res)
    l.append(res)


def workflow():
    start = time.time()

    parallel_res = []
    threads = []

    for url in urls:
        t = threading.Thread(target=post, args=(url, json.dumps(req), parallel_res))
        threads.append(t)

    for t in threads:
        t.start()

    for t in threads:
        t.join()

    result = []

    for i in parallel_res:
        print(i)
        result.append(json.loads(json.loads(i)))

    print("result::::::::::::::::::")
    print(type(result))

    res = requests.post(margin_balance_url, data=json.dumps(result), headers=headers).text
    print("res:::::::::::::::::")
    print(res)
    # print("This request uses %d ms" % int((time.time() - start) * 1000))
    return int((time.time() - start) * 1000)




@app.route('/hi')
def index():
    lats = []
    for i in range(1):
        lat = workflow()
        lats.append(lat)

    # print(lats)
    # print(sum(lats[1:]) / (len(lats) - 1))
    # print("This request uses %d ms" %(sum(lats[1:]) / (len(lats) - 1)))
    return {
        "msg": "success",
        "data": "welcome"
    }


if __name__ == "__main__":
    app.run()