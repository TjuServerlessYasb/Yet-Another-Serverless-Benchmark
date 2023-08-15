import json
import numpy as np
from scipy.optimize import linprog


def PrintRes(res):
    return {
        "OptimalValue": res.fun,
        "OptimalSolution": res.x
    }


def handle(req):
    """handle a request to the function
        Args:
            req (str): request body
    """
    event = json.loads(req)
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
    return PrintRes(res)
