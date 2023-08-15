from ray import serve
from typing import List, Dict

import json
import numpy as np
from scipy.optimize import linprog





@serve.deployment(num_replicas=1, ray_actor_options={"num_cpus": 1, "num_gpus": 0})
class LinearProgrammingService(object):
    # def __init__(self):
    def LinearProgramming(self, body: Dict):
        print(123)
        try:

            event = body
            MinOrMax = event['MinOrMax']
            target = event['target']
            A = event['A']
            b = event['b']
            bounds = event['bounds']
            print("线性规划求解器:")
            if MinOrMax == 'min':
                pass
            elif MinOrMax == 'max':
                target = np.array(target) * (-1)
            # minimize
            res = linprog(target, A, b, bounds=bounds)

        except Exception as e:
            print(e)
            print(e.__traceback__.tb_frame.f_globals["__file__"])  # 发生异常所在的文件
            print(e.__traceback__.tb_lineno)  # 发生异常所在的行数
        else:
            print("success")

        return {
            "OptimalValue": res.fun,
            "OptimalSolution": res.x
        }

