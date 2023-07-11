from ray import serve
from typing import List, Dict






@serve.deployment(num_replicas=1, ray_actor_options={"num_cpus": 1, "num_gpus": 0})
class EigenService(object):
    # def __init__(self):
    def Eigen(self, body: Dict):
        print(123)
        try:

            event = body
            matrix = event["matrix"]
            eigenvalue, featurevector = np.linalg.eig(matrix)
            print("特征值：", eigenvalue)
            print("特征向量：", featurevector)

        except Exception as e:
            print(e)
            print(e.__traceback__.tb_frame.f_globals["__file__"])  # 发生异常所在的文件
            print(e.__traceback__.tb_lineno)  # 发生异常所在的行数
        else:
            print("success")

        return {
            "eigenvalue": eigenvalue,
            "featurevector": featurevector
        }

