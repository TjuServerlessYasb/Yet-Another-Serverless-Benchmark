from ray import serve
from typing import List, Dict
from time import time
import string
import random

def gen_random_digits(i):
    return "".join(random.sample(string.digits, i))


@serve.deployment(num_replicas=1, ray_actor_options={"num_cpus": 1, "num_gpus": 0})
class MrUploadUniqueIdService(object):
    # def __init__(self):
    def MrUploadUniqueId(self, body1: Dict):
        print(123)
        try:
            start = time()

            event = body1

            response = {"time": {"mr-upload-unique-id": {"start_time": start}}}

            machine_id = gen_random_digits(2)
            timestamp = str(int(time() * 1000) - 1514764800000)[-11:]
            index_id = gen_random_digits(3)
            review_id = machine_id + timestamp + index_id

            response["body"] = {"review_id": review_id}
            response["time"]["mr-upload-unique-id"]["end_time"] = time()
            print(response)
        except Exception as e:
            print(e)
            print(e.__traceback__.tb_frame.f_globals["__file__"])  # 发生异常所在的文件
            print(e.__traceback__.tb_lineno)  # 发生异常所在的行数
        else:
            print("success")


        return response

