import json
import numpy as np
from scipy.optimize import linprog

'''
    输入条件均为小于或小于等于
    Derivation: https://blog.csdn.net/chengyikang20/article/details/83685589
    Params:
        MinOrMax(String): 'min'/'max'
    Example:
        1. 
            Question: min f=-1*x0+4*x1
            Condition:
                -3*x0+1*x1≤6
                1*x0+2*x1≤4
                x1≥-3
        2. 
            Question: max f=-1*x0+4*x1
            Condition:
                -3*x0+1*x1≤6
                1*x0+2*x1≤4
                x1≥-3
'''


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
    PrintRes(res)
