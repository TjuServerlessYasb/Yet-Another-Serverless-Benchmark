import json

import ray
import requests
from fastapi import FastAPI
from ray import serve
from ray.serve.handle import RayServeDeploymentHandle
from wc.service.map import MapService
from wc.service.reduce import ReduceService
from wc.model.post import PostBodyMap,PostBodyReduce,PostStr

app = FastAPI()


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
    async def map(self, req: PostBodyMap):
        print("map")
        result = await self._map_handle.Mapper.remote(req)
        return {"message": 200}

    @app.post("/wc/reduce")
    async def reduce(self, req: PostBodyReduce):
        print("reduce")
        result = await self._reduce_handle.Reducer.remote(req)
        return {"message": 200}

    @app.get("/wc/test")
    async def root(self):
        return "Hello from 111!"

map_handle = MapService.bind()
reduce_handle = ReduceService.bind()

ingress = WordCount.bind(map_handle,reduce_handle)

