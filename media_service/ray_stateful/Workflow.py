import requests
import threading
import random
import string

import json
import time
from flask import Flask

app = Flask(__name__)

headers = {
    "Content-Type": "application/json",
    "accept": "application/json",
    }


funcsOne = ["upload_user_id","upload_movie_id","upload_text","upload_unique_id"]
urlsOne = [f"http://10.244.0.183:8000/ms/{func}" for func in funcsOne]

funcsTwo = ["store_review_service","upload_user_review","upload_movie_review_handle"]
urlsTwo = [f"http://10.244.0.183:8000/ms/{func}" for func in funcsTwo]




def gen_random_string(i):
    choices = string.ascii_letters + string.digits
    return "".join([choices[random.randint(0, len(choices)-1)] for j in range(i)])

movie_titles = []
with open("movie_titles.csv", "r") as f:
    movie_titles = f.readlines()

def generate_data():
    user_index = str(random.randint(1, 1000))
    review = {
        "username": "username_" + user_index,
        "password": "password_" + user_index,
        "title": movie_titles[random.randint(0, len(movie_titles)-1)].strip(),
        "rating": random.randint(0, 10),
        "text": gen_random_string(256)
    }

    return review


def post(url, data, l):
    res = requests.post(url, data=data, headers=headers).text
    print()
    print(url)
    print(res)
    l.append(res)


def workflow():
    try:
        review = generate_data()

        start = time.time()
        compose_res = requests.post("http://10.244.0.183:8000/ms/compose_review", data=json.dumps(review), headers=headers).text

        compose_res = json.loads(json.loads(compose_res))
        print("compose_res:")
        print(compose_res)
        parallel_res = []
        threads = []
        for url in urlsOne:
            t = threading.Thread(target=post, args=(url, json.dumps(compose_res), parallel_res))
            threads.append(t)

        for t in threads:
            t.start()

        for t in threads:
            t.join()

        result = []
        for i in parallel_res:
            print(i)
            result.append(json.loads(json.loads(i)))

        print("4 function:")
        print(result)
        # print(type(result))

        mr_res = requests.post("http://10.244.0.183:8000/ms/mr_compose_and_upload", data=json.dumps(result),
                              headers=headers).text

        mr_res = json.loads(json.loads(mr_res))
        print("mr_res:")
        print(mr_res)

        parallel_res = []
        threads = []
        for url in urlsTwo:
            t = threading.Thread(target=post, args=(url, json.dumps(mr_res), parallel_res))
            threads.append(t)

        for t in threads:
            t.start()

        for t in threads:
            t.join()

        print("3 function:")
        print(parallel_res)


    except Exception as e:
        print(e)
        print(e.__traceback__.tb_frame.f_globals["__file__"])  # 发生异常所在的文件
        print(e.__traceback__.tb_lineno)  # 发生异常所在的行数
    else:
        print("success")
    return int((time.time() - start) * 1000)


@app.route('/hi')
def index():
    lats = []
    for i in range(1):
        lat = workflow()
        lats.append(lat)

    # print(lats)
    # print(sum(lats[1:]) / (len(lats) - 1))
    # print("This request uses %d so" %(sum(lats[1:]) / (len(lats) - 1)))
    return {
        "msg": "success",
        "data": "welcome"
    }


if __name__ == "__main__":
    app.run()