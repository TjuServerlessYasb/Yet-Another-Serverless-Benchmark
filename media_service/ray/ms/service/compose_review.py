from ray import serve
from typing import List, Dict
import time
import json

from ms.model.post import PostItem
from fastapi import Body

arguments = ["title", "text", "username", "password", "rating"]

@serve.deployment(num_replicas=1, ray_actor_options={"num_cpus": 1, "num_gpus": 0})
class ComposeReviewService(object):
    # def __init__(self):
    def ComposeReview(self, body: Dict):
        print(123)
        try:
            start = time.time()
            event = body
            response = {"time": {"compose-review": {"start_time": start}}}

            complete = False
            try:
                for arg in arguments:
                    if event[arg] == '':
                        break
                complete = True
            except Exception as e:
                pass

            if complete:
                response["body"] = event
            else:
                response["body"] = "Incomplete arguments"

            response["time"]["compose-review"]["end_time"] = time.time()
            print(response)
        except Exception as e:
            print(e)
            print(e.__traceback__.tb_frame.f_globals["__file__"])  # 发生异常所在的文件
            print(e.__traceback__.tb_lineno)  # 发生异常所在的行数
        else:
            print("success")


        return response

