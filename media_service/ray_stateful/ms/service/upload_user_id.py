from ray import serve
from typing import List, Dict
import ray
from time import time
import pymongo
from pymemcache.client.base import Client
import json

mongo_url = "mongodb://user-mongodb.movie-reviewing.svc.cluster.local:27017/"
memcache_url = "user-memcached.movie-reviewing.svc.cluster.local:11211"

mc = Client(memcache_url)

arguments = ["title", "text", "username", "password", "rating"]

@serve.deployment(num_replicas=1, ray_actor_options={"num_cpus": 1, "num_gpus": 0})
class UploadUserIdService(object):
    # def __init__(self):
    def UploadUserId(self, body1: Dict):
        print(123)
        try:
            start = time()

            myclient = pymongo.MongoClient(mongo_url)
            mydb = myclient['user']
            mycol = mydb["user"]
            print(body1)
            event = body1
            body = ''
            username = ''
            response = {"time": {"upload-user-id": {"start_time": start}}}
            try:
                username = event["body"]["username"]
            except Exception as e:
                body = 'Incomplete arguments'

            if username:
                user_id = -1
                mmc_user_id = mc.get(username + ":user_id")
                if mmc_user_id != None:
                    user_id = mmc_user_id
                    body = {"user_id": user_id}
                else:
                    myquery = {"username": username}
                    mydoc = mycol.find(myquery)
                    print("query num:",mycol.count_documents(myquery))
                    if mycol.count_documents(myquery) > 0:
                        it = mydoc.next()
                        user_id = it["user_id"]
                        body = {"user_id": user_id}
                        mc.set(username + ":user_id", user_id)
                    else:
                        body = 'No user ' + username

            response["body"] = body

            response["time"]["upload-user-id"]["end_time"] = time()
            print(response)

        except Exception as e:
            print(e)
            print(e.__traceback__.tb_frame.f_globals["__file__"])  # 发生异常所在的文件
            print(e.__traceback__.tb_lineno)  # 发生异常所在的行数
        else:
            print("success")


        return ray.put(response)
