import json
import ray
import requests
from fastapi import Body, FastAPI
from typing import List, Dict
from ray import serve
from ray.serve.handle import RayServeDeploymentHandle

from so.service.arithmetic_arranger import ArrangedProblemsService
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
class MediaService:
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
        result = await self._arithmetic_arranger_handle.ArrangedProblems.remote(body)
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


arithmetic_arranger_handle = ArrangedProblemsService.bind()
curve_fitting_handle = CurveFittingService.bind()
eigen_handle = EigenService.bind()
linear_programming_handle = LinearProgrammingService.bind()
prob_calculator_handle = ProbCalculatorService.bind()
time_calculator_handle = TimeCalculatorService.bind()


ingress = MediaService.bind(arithmetic_arranger_handle, curve_fitting_handle,eigen_handle,linear_programming_handle,prob_calculator_handle,time_calculator_handle)
