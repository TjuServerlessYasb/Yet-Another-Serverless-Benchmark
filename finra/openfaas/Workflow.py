import requests
import threading

import json
import time
from flask import Flask

app = Flask(__name__)

margin_balance_url = "http://127.0.0.1:31119/function/margin-balance"

funcs = ["marketdata", "lastpx", "side", "trddate", "volume"]

urls = [f"http://127.0.0.1:31119/function/{func}" for func in funcs]

req = '{"body":{ "portfolioType":"S&P", "portfolio":"1234"}}'


def post(url, data, l):
    res = requests.post(url, data).text
    l.append(res)


def workflow():
    start = time.time()

    parallel_res = []
    threads = []

    for url in urls:
        t = threading.Thread(target=post, args=(url, req, parallel_res))
        threads.append(t)

    for t in threads:
        t.start()

    for t in threads:
        t.join()

    res = requests.post(margin_balance_url, data=json.dumps(parallel_res)).text
    # print("This request uses %d ms" % int((time.time() - start) * 1000))
    return int((time.time() - start) * 1000)




@app.route('/hi')
def index():
    lats = []
    for i in range(11):
        lat = workflow()
        lats.append(lat)

    # print(lats)
    # print(sum(lats[1:]) / (len(lats) - 1))
    print("This request uses %d ms" %(sum(lats[1:]) / (len(lats) - 1)))
    return {
        "msg": "success",
        "data": "welcome"
    }


if __name__ == "__main__":
    app.run()