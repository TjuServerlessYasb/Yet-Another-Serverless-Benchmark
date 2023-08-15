import numpy as np
import json


def handle(req):
    event = json.loads(req)
    matrix = event["matrix"]
    eigenvalue, featurevector = np.linalg.eig(matrix)
    return {
        "eigenvalue": eigenvalue,
        "featurevector": featurevector
    }
