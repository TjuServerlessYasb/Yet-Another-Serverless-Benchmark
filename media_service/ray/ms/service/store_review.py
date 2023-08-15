from ray import serve
from typing import List, Dict


from time import time
import pymongo
import json


arguments = set(["review_id", "timestamp", "user_id", "movie_id", "text", "rating"])

@serve.deployment(num_replicas=1, ray_actor_options={"num_cpus": 1, "num_gpus": 0})
class StoreReviewService(object):
    # def __init__(self):
    def StoreReview(self, body1: Dict):
        print(123)
        try:
            start = time()

            myclient = pymongo.MongoClient("mongodb://review-storage-mongodb.movie-reviewing.svc.cluster.local:27017/")
            mydb = myclient["review"]
            mycol = mydb["review"]

            event = body1
            response = {"time": {"store-review": {"start_time": start}}}

            if set(event["body"].keys()) == arguments:
                response["time"].update(event["time"])
                mycol.insert_one(event["body"])
            else:
                response['body'] = 'Incomplete arguments'

            response["time"]["store-review"]["end_time"] = time()
            print(response)
        except Exception as e:
            print(e)
            print(e.__traceback__.tb_frame.f_globals["__file__"])  # 发生异常所在的文件
            print(e.__traceback__.tb_lineno)  # 发生异常所在的行数
        else:
            print("success")


        return response

