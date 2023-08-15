from ray import serve
from typing import List, Dict

import copy
import random
import json


class Hat:

    def __init__(self, **kwargs):
        self.contents = []
        for key, value in kwargs.items():
            for _ in range(value):
                self.contents.append(key)

    def draw(self, number):
        if number > len(self.contents):
            return self.contents
        balls = []
        for _ in range(number):
            choice = random.randrange(len(self.contents))
            balls.append(self.contents.pop(choice))
        return balls


def experiment(hat, expected_balls, num_balls_drawn, num_experiments):
    expected_no_of_balls = []
    for key in expected_balls:
        expected_no_of_balls.append(expected_balls[key])
    successes = 0

    for _ in range(num_experiments):
        new_hat = copy.deepcopy(hat)
        balls = new_hat.draw(num_balls_drawn)

        no_of_balls = []
        for key in expected_balls:
            no_of_balls.append(balls.count(key))

        if no_of_balls >= expected_no_of_balls:
            successes += 1

    return successes / num_experiments


@serve.deployment(num_replicas=1, ray_actor_options={"num_cpus": 1, "num_gpus": 0})
class ProbCalculatorService(object):
    # def __init__(self):
    def ProbCalculator(self, body: Dict):
        print(123)
        try:

            event = body
            hat = Hat(**event["hat"])
            probability = experiment(
                hat=hat,
                expected_balls=event["expected_balls"],
                num_balls_drawn=event["num_balls_drawn"],
                num_experiments=event["num_experiments"]
            )


        except Exception as e:
            print(e)
            print(e.__traceback__.tb_frame.f_globals["__file__"])  # 发生异常所在的文件
            print(e.__traceback__.tb_lineno)  # 发生异常所在的行数
        else:
            print("success")

        return probability

