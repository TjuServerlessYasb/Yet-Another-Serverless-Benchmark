from ray import serve
from typing import List, Dict

from time import time
import pymongo
from pymemcache.client.base import Client
import json
import hashlib
import ray

mongo_url = "mongodb://movie-id-mongodb.movie-reviewing.svc.cluster.local:27017/"
memcache_url = "movie-id-memcached.movie-reviewing.svc.cluster.local:11211"

mc = Client(memcache_url)

def hash_key(title):
    m = hashlib.md5()
    m.update(title.encode("utf-8"))
    return m.hexdigest()

@serve.deployment(num_replicas=1, ray_actor_options={"num_cpus": 1, "num_gpus": 0})
class UploadMovieIdService(object):
    # def __init__(self):
    def UploadMovieId(self, body1: Dict):
        print(123)
        try:
            start = time()

            myclient = pymongo.MongoClient(mongo_url)
            mydb = myclient['movie-id']
            mycol = mydb["movie-id"]
            print(body1)
            event = body1
            body = ''
            title = ''
            title_hash = ''
            rating = -1
            response = {"time": {"upload-movie-id": {"start_time": start}}}
            try:
                title = event["body"]["title"]
                title_hash = hash_key(title)
                rating = int(event["body"]["rating"])
            except Exception as e:
                response['body'] = 'Incomplete arguments'

            if title and rating > -1:
                movie_id = ''
                mmc_movie_id = mc.get(title_hash)
                if mmc_movie_id != None:
                    movie_id = mmc_movie_id
                    response["body"] = {"movie_id": movie_id, 'rating': rating}
                else:
                    myquery = {"title": title}
                    mydoc = mycol.find(myquery)
                    print("query num:", mycol.count_documents(myquery))
                    if mycol.count_documents(myquery) > 0:
                        it = mydoc.next()
                        movie_id = it["movie_id"]
                        response["body"] = {"movie_id": movie_id, 'rating': rating}
                        mc.set(title_hash, movie_id)
                    else:
                        response["body"] = 'No movie ' + title

            response["time"]["upload-movie-id"]["end_time"] = time()

        except Exception as e:
            print(e)
            print(e.__traceback__.tb_frame.f_globals["__file__"])  # 发生异常所在的文件
            print(e.__traceback__.tb_lineno)  # 发生异常所在的行数
        else:
            print("success")


        return ray.put(response)

