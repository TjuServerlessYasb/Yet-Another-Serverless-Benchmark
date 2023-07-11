import requests
import threading
import random
import string
import json
import time

compose_review_url = "http://127.0.0.1:31119/function/compose-review"
upload_user_id_url = "http://127.0.0.1:31119/function/upload-user-id"
upload_movie_id_url = "http://127.0.0.1:31119/function/upload-movie-id"
mr_upload_text_url = "http://127.0.0.1:31119/function/mr-upload-text"
mr_upload_unique_id_url = "http://127.0.0.1:31119/function/mr-upload-unique-id"
mr_compose_and_upload_url = "http://127.0.0.1:31119/function/mr-compose-and-upload"
store_review_url = "http://127.0.0.1:31119/function/store-review"
upload_user_review_url = "http://127.0.0.1:31119/function/upload-user-review"
upload_movie_review_url = "http://127.0.0.1:31119/function/upload-movie-review"

funcs = ["compose-review", "upload-user-id", "upload-movie-id", "mr-upload-text", "mr-upload-unique-id", 
    "mr-compose-and-upload", "store-review", "upload-user-review", "upload-movie-review"]

def gen_random_string(i):
    choices = string.ascii_letters + string.digits
    return "".join([choices[random.randint(0, len(choices)-1)] for j in range(i)])

def post(url, data, l):
    res = requests.post(url, data).text
    l.append(res)
    print(url,res)

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

    return json.dumps(review)

def workflow():
    review = generate_data()

    start = time.time()
    compose_res = requests.post(compose_review_url, data=review).text

    parallel_res = []
    threads = []
    for url in [upload_user_id_url, upload_movie_id_url, mr_upload_text_url, mr_upload_unique_id_url]:
        t = threading.Thread(target=post, args=(url, compose_res, parallel_res))
        threads.append(t)
    
    for t in threads:
        t.start()
    
    for t in threads:
        t.join()

    # print(parallel_res)

    compose_and_upload_res = requests.post(mr_compose_and_upload_url, data=json.dumps(parallel_res)).text

    print(compose_and_upload_res)
    print(type(compose_and_upload_res))

    parallel_res = []
    threads = []
    for url in [store_review_url, upload_user_review_url, upload_movie_review_url]:
        t = threading.Thread(target=post, args=(url, compose_and_upload_res, parallel_res))
        threads.append(t)
    
    for t in threads:
        t.start()
    
    for t in threads:
        t.join()
    print("This request uses %d so" % int((time.time() - start) * 1000))
    return int((time.time()-start)*1000)

    
    funcs_time = {}
    for f in funcs:
        funcs_time[f] = -1
    
    try:
        if len(parallel_res) != 3:
            print("Something wrong in the final stage")
        else:
            for res in parallel_res:
                res = json.loads(res)
                for k, v in res["time"].items():
                    funcs_time[k] = int((v["end_time"]-v["start_time"])*1000)
                    if funcs_time[k] == 0:
                        funcs_time[k] = round((v["end_time"]-v["start_time"])*1000, 2)
            print("Details:")
            for f in funcs:
                print("  %s: %s so" % (f, str(funcs_time[f])))
    except Exception as e:
        print("Something wrong in the final stage")
        print(e)

if __name__ == '__main__':
    lats = []
    for i in range(1):
        lat = workflow()
        lats.append(lat)

    # print(lats)
    # print(sum(lats[1:])/(len(lats)-1))
