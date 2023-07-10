import numpy as np
import json

eigenvalue, featurevector = np.linalg.eig(mat)

print("特征值：", eigenvalue)
print("特征向量：", featurevector)


def handle(req):
    event = json.loads(req)
    matrix = event["matrix"]
    eigenvalue, featurevector = np.linalg.eig(matrix)
    return {
        "eigenvalue": eigenvalue,
        "featurevector": featurevector
    }
