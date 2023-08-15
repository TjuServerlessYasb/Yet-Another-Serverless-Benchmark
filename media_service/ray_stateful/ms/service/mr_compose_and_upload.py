from ray import serve
from typing import List, Dict
import ray
from time import time


@serve.deployment(num_replicas=1, ray_actor_options={"num_cpus": 1, "num_gpus": 0})
class MrComposeAndUploadService(object):
    # def __init__(self):
    def MrComposeAndUpload(self, body1: List):
        print(123)
        try:
            start = time()
            print("body1:")
            print(body1)
            events = body1
            print(len(events))
            body = {}
            response = {"time": {"mr-compose-and-upload": {"start_time": start}}}

            if len(events) < 4:
                body = 'Incomplete arguments'
            else:
                for ev in events:
                    event = ray.get(ray.get(ev))
                    body.update(event["body"])
                    response["time"].update(event["time"])
                body["timestamp"] = int(time() * 1000)
                # body = 'Incomplete arguments'

            response["body"] = body
            response["time"]["mr-compose-and-upload"]["end_time"] = time()
            print(response)
        except Exception as e:
            print(e)
            print(e.__traceback__.tb_frame.f_globals["__file__"])  # 发生异常所在的文件
            print(e.__traceback__.tb_lineno)  # 发生异常所在的行数
        else:
            print("success")

        return ray.put(response)
