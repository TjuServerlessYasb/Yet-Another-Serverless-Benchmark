import json

import ray
import requests
from fastapi import FastAPI
from ray import serve
from ray.serve.handle import RayServeDeploymentHandle
from wc.service.map import MapService
from wc.service.reduce import ReduceService
from wc.model.post import PostBodyMap,PostBodyReduce,PostStr
from typing import List, Dict
import threading
import asyncio

app = FastAPI()


async def mappost1(data, l):
    try:
        print(data)
        res = await WordCount.map(data)
        print("my result :", await res)
        l.update(await res)
    except Exception as e:
        print(e)
        print(e.__traceback__.tb_frame.f_globals["__file__"])  # 发生异常所在的文件
        print(e.__traceback__.tb_lineno)  # 发生异常所在的行数
    else:
        print("success")




@serve.deployment()
@serve.ingress(app)
class WordCount:
    def __init__(
        self,
        map_handle: RayServeDeploymentHandle,
        reduce_handle: RayServeDeploymentHandle,
    ):
        self._map_handle = map_handle
        self._reduce_handle = reduce_handle

    @app.post("/wc/map")
    async def map(self, req: Dict):
        try:
            print("map")
            shuffleResult = await self._map_handle.Mapper.remote(req)
        except Exception as e:
            print(e)
            print(e.__traceback__.tb_frame.f_globals["__file__"])  # 发生异常所在的文件
            print(e.__traceback__.tb_lineno)  # 发生异常所在的行数
        else:
            print("success")

        return shuffleResult

    @app.post("/wc/reduce")
    async def reduce(self, req: Dict):
        print("reduce")
        result = await self._reduce_handle.Reducer.remote(req)
        return result


    @app.get("/wc/workflow")
    async def root(self):
        try:
            # curl http://10.244.0.183:8000/wc/workflow
            mapper_num = 5
            reducer_num = 5
            tasks = []
            for i in range(mapper_num):
                req = {"input_name": "data-500m", "input_part": i, "reduce_num": reducer_num}
                task = asyncio.ensure_future(self.map(req))
                tasks.append(task)
            res = await asyncio.gather(*tasks)


            tasks = []
            for i in range(reducer_num):
                req = {"input_name": "data-500m", "input_num": mapper_num, "reduce_part": i, "shuffleResult": res}
                task = asyncio.ensure_future(self.reduce(req))
                tasks.append(task)
            res1 = await asyncio.gather(*tasks)
            print(res1)


        except Exception as e:
            print(e)
            print(e.__traceback__.tb_frame.f_globals["__file__"])  # 发生异常所在的文件
            print(e.__traceback__.tb_lineno)  # 发生异常所在的行数
        else:
            print("success")
        return {"message": 200}

    @app.get("/wc/test")
    async def root(self):
        return "Hello from 111!"

map_handle = MapService.bind()
reduce_handle = ReduceService.bind()

ingress = WordCount.bind(map_handle,reduce_handle)

