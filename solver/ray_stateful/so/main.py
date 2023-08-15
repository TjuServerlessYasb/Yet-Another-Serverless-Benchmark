import json
import ray
import requests
from fastapi import Body, FastAPI
from typing import List, Dict
from ray import serve
from ray.serve.handle import RayServeDeploymentHandle

from so.service.arithmetic_arranger import ArithmeticArrangerService
from so.service.curve_fitting import CurveFittingService
from so.service.eigen import EigenService
from so.service.linear_programming import LinearProgrammingService
from so.service.prob_calculator import ProbCalculatorService
from so.service.time_calculator  import TimeCalculatorService


import asyncio
import random
import string
import time

app = FastAPI()



@serve.deployment()
@serve.ingress(app)
class Solver:
    def __init__(
            self,
            arithmetic_arranger_handle: RayServeDeploymentHandle,
            curve_fitting_handle: RayServeDeploymentHandle,
            eigen_handle: RayServeDeploymentHandle,
            linear_programming_handle: RayServeDeploymentHandle,
            prob_calculator_handle: RayServeDeploymentHandle,
            time_calculator_handle: RayServeDeploymentHandle,


    ):
        self._arithmetic_arranger_handle = arithmetic_arranger_handle
        self._curve_fitting_handle = curve_fitting_handle
        self._eigen_handle = eigen_handle
        self._linear_programming_handle = linear_programming_handle
        self._prob_calculator_handle = prob_calculator_handle
        self._time_calculator_handle = time_calculator_handle



    @app.post("/so/arithmetic_arranger")
    async def arithmetic_arranger(self, body: Dict):
        result = await self._arithmetic_arranger_handle.ArithmeticArranger.remote(body)
        return result

    @app.post("/so/curve_fitting")
    async def curve_fitting(self, body: Dict):
        result = await self._curve_fitting_handle.CurveFitting.remote(body)
        return result

    @app.post("/so/eigen")
    async def eigen(self, body: Dict):
        result = await self._eigen_handle.Eigen.remote(body)
        return result

    @app.post("/so/linear_programming")
    async def linear_programming(self, body: Dict):
        result = await self._linear_programming_handle.LinearProgramming.remote(body)
        return result

    @app.post("/so/prob_calculator")
    async def prob_calculator(self, body: Dict):
        result = await self._prob_calculator_handle.ProbCalculator.remote(body)
        return result

    @app.post("/so/time_calculator")
    async def time_calculator(self, body: Dict):
        result = await self._time_calculator_handle.TimeCalculator.remote(body)
        return result

    @app.get("/so/workflow")
    async def root(self):
        try:
            # curl http://10.244.0.195:8000/so/workflow
            text1 = {"problems":["32 + 698", "3801 - 2", "45 + 43", "123 + 49"]}
            arithmetic_arranger_res = await self.arithmetic_arranger(text1)
            print(await arithmetic_arranger_res)

            text1 = {"X":[150, 200, 250, 350, 300, 400, 600],"y":[6450, 7450, 8450, 9450, 11450, 15450, 18450]}
            curve_fitting_res = await self.curve_fitting(text1)
            print(await curve_fitting_res)

            text1 = {"matrix":[[-1, 1, 0],[-4, 3, 0],[1, 0, 2]]}
            eigen_res = await self.eigen(text1)
            print(await eigen_res)

            text1 = {"MinOrMax":"min","target":[-1,4],"A":[[-3,1],[1,2]],"b":[6,4],"bounds":[[None,None],[-3,None]]}
            linear_programming_res = await self.linear_programming(text1)
            print(await linear_programming_res)

            text1 = {"hat":{"blue":4,"red":2,"green":6},"expected_balls":{"blue":2,"red":1},"num_balls_drawn":4,"num_experiments":3000}
            prob_calculator_res = await self.prob_calculator(text1)
            print(await prob_calculator_res)

            text1 = {"start":"11:06 PM","duration":"2:02"}
            time_calculator_res_res = await self.time_calculator(text1)
            print(await time_calculator_res_res)


        except Exception as e:
            print(e)
            print(e.__traceback__.tb_frame.f_globals["__file__"])  # 发生异常所在的文件
            print(e.__traceback__.tb_lineno)  # 发生异常所在的行数
        else:
            print("success")
        return {"message": 200}

arithmetic_arranger_handle = ArithmeticArrangerService.bind()
curve_fitting_handle = CurveFittingService.bind()
eigen_handle = EigenService.bind()
linear_programming_handle = LinearProgrammingService.bind()
prob_calculator_handle = ProbCalculatorService.bind()
time_calculator_handle = TimeCalculatorService.bind()


ingress = Solver.bind(arithmetic_arranger_handle, curve_fitting_handle,eigen_handle,linear_programming_handle,prob_calculator_handle,time_calculator_handle)
