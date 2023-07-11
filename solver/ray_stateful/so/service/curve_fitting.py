from ray import serve
from typing import List, Dict


from scipy.optimize import curve_fit



@serve.deployment(num_replicas=1, ray_actor_options={"num_cpus": 1, "num_gpus": 0})
class CurveFittingService(object):
    # def __init__(self):
    def CurveFitting(self, body: Dict):
        print(123)
        try:

            event = body
            X = event['X']
            y = event['y']

            def func(x, a, b):
                y = a * x + b
                return y
            popt, pcov = curve_fit(func, X, y)

        except Exception as e:
            print(e)
            print(e.__traceback__.tb_frame.f_globals["__file__"])  # 发生异常所在的文件
            print(e.__traceback__.tb_lineno)  # 发生异常所在的行数
        else:
            print("success")


        return {"popt":popt, "pcov":pcov}

