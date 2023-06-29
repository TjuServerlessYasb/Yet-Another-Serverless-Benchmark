from ray import serve
from typing import List, Dict
import ray
from time import time

@serve.deployment(num_replicas=1, ray_actor_options={"num_cpus": 1, "num_gpus": 0})
class MrUploadTextService(object):
    # def __init__(self):
    def MrUploadText(self, body1: Dict):
        print(123)
        try:
            start = time()

            event = body1

            response = {"time": {"mr-upload-text": {"start_time": start}}}
            text = ''
            try:
                text = event["body"]["text"]
                response["time"].update(event["time"])
            except Exception as e:
                response["body"] = 'Incomplete arguments'

            if text:
                response["body"] = {"text": text}

            response["time"]["mr-upload-text"]["end_time"] = time()
            print(response)

        except Exception as e:
            print(e)
            print(e.__traceback__.tb_frame.f_globals["__file__"])  # 发生异常所在的文件
            print(e.__traceback__.tb_lineno)  # 发生异常所在的行数
        else:
            print("success")


        return ray.put(response)

