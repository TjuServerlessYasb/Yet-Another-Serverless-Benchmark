import json
from scipy.optimize import curve_fit


def handle(req):
    """handle a request to the function
        Args:
            req (str): request body
    """
    event = json.loads(req)
    X = event['X']
    y = event['y']

    def func(x, a, b):
        y = a * x + b
        return y

    try:
        popt, pcov = curve_fit(func, X, y)
    except Exception as e:
        print(e)
        return e
    else:
        return popt, pcov
