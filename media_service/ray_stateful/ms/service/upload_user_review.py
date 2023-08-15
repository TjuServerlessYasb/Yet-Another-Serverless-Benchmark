from ray import serve
from typing import List, Dict


from time import time
import pymongo
import json
import ray



@serve.deployment(num_replicas=1, ray_actor_options={"num_cpus": 1, "num_gpus": 0})
class UploadUserReviewService(object):
    # def __init__(self):
    def UploadUserReview(self, body1: Dict):
        print(123)
        try:
            start = time()

            myclient = pymongo.MongoClient("mongodb://user-review-mongodb.movie-reviewing.svc.cluster.local:27017/")
            mydb = myclient["user-review"]
            mycol = mydb["user-review"]

            event = body1
            print(event)
            response = {"time": {"upload-user-review": {"start_time": start}}}

            try:
                user_id = event["body"]["user_id"]
                review_id = event["body"]["review_id"]
                timestamp = event["body"]["timestamp"]

                myquery = {"user_id": user_id}
                mydoc = mycol.find(myquery)
                if mycol.count_documents(myquery) > 0:
                    reviews = json.loads(mydoc.next()["reviews"])
                    reviews.append((review_id, timestamp))
                    reviews_update = {"$set": {"reviews": json.dumps(reviews)}}
                    mycol.update_one(myquery, reviews_update)
                else:
                    body = {"user_id": user_id, "reviews": json.dumps([(review_id, timestamp)])}
                    mycol.insert_one(body)
            except Exception as e:
                response['body'] = 'Incomplete arguments'

            response["time"]["upload-user-review"]["end_time"] = time()
        except Exception as e:
            print(e)
            print(e.__traceback__.tb_frame.f_globals["__file__"])  # 发生异常所在的文件
            print(e.__traceback__.tb_lineno)  # 发生异常所在的行数
        else:
            print("success")


        return response

