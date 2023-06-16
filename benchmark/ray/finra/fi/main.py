import json

import ray
import requests
from fastapi import Body, FastAPI
from typing import List, Dict
from ray import serve
from ray.serve.handle import RayServeDeploymentHandle
from fi.service.lastpx import LastpxService
from fi.service.side import SideService
from fi.service.trddate import TrddateService
from fi.service.volume import VolumeService
from fi.service.yfinance import YfinanceService
from fi.service.marginBalance import MarginBalanceService
from fi.service.marketdata import MarketdataService

from fi.model.post import PostStr, PostItem

app = FastAPI()


@serve.deployment()
@serve.ingress(app)
class Finra:
    def __init__(
            self,
            lastpx_handle: RayServeDeploymentHandle,
            side_handle: RayServeDeploymentHandle,
            trddate_handle: RayServeDeploymentHandle,
            volume_handle: RayServeDeploymentHandle,
            yfinance_handle: RayServeDeploymentHandle,
            marginBalance_handle: RayServeDeploymentHandle,
            marketdataService_handle: RayServeDeploymentHandle,
    ):
        self._lastpx_handle = lastpx_handle
        self._side_handle = side_handle
        self._trddate_handle = trddate_handle
        self._volume_handle = volume_handle
        self._yfinance_handle = yfinance_handle
        self._marginBalance_handle = marginBalance_handle
        self._marketdataService_handle = marketdataService_handle


    @app.post("/fi/lastpx")
    async def root1(self, body: Dict):
        result = await self._lastpx_handle.Lastpx.remote(body)
        r = json.dumps(await result)
        print(await result)
        return r


    @app.post("/fi/side")
    async def root2(self, body: Dict):
        result = await self._side_handle.Side.remote(body)
        r = json.dumps(await result)
        print(await result)
        return r

    @app.post("/fi/trddate")
    async def root3(self, body: Dict):
        result = await self._trddate_handle.Trddate.remote(body)
        r = json.dumps(await result)
        print(await result)
        return r

    @app.post("/fi/volume")
    async def root4(self, body: Dict):
        result = await self._volume_handle.Volume.remote(body)
        r = json.dumps(await result)
        print(await result)
        return r

    @app.post("/fi/yfinance")
    async def root5(self, body: Dict):
        result = await self._yfinance_handle.Yfinance.remote(body)
        r = json.dumps(await result)
        print(await result)
        return r


    @app.post("/fi/volume")
    async def root6(self, body: Dict):
        result = await self._volume_handle.Volume.remote(body)
        r = json.dumps(await result)
        print(await result)
        return r

    @app.post("/fi/marginBalance")
    async def root7(self, dic: List):
        result = await self._marginBalance_handle.MarginBalance.remote(dic)
        r = json.dumps(await result)
        print(await result)
        return r

    @app.post("/fi/marketdata")
    async def root8(self, dic: Dict):
        result = await self._marketdataService_handle.Marketdata.remote(dic)
        r = json.dumps(await result)
        print(await result)
        return r

    # @app.post("/fi/lastpx")
    # async def root(self, body: PostItem = Body(embed=True)):
    #     result = await self._lastpx_handle.Lastpx.remote(body)
    #     print(result)
    #     return {"status ": 200}
    #
    # @app.post("/fi/side")
    # async def root(self, body: PostItem = Body(embed=True)):
    #     result = await self._side_handle.Side.remote(body)
    #     print(result)
    #     return {"status ": 200}
    #
    # @app.post("/fi/trddate")
    # async def root(self, body: PostItem = Body(embed=True)):
    #     result = await self._trddate_handle.Trddate.remote(body)
    #     print(result)
    #     return {"status ": 200}
    #
    # @app.post("/fi/volume")
    # async def root(self, body: PostItem = Body(embed=True)):
    #     result = await self._volume_handle.Volume.remote(body)
    #     print(result)
    #     return {"status ": 200}
    #
    # @app.post("/fi/yfinance")
    # async def root(self, req: PostStr):
    #     result = await self._lastpx_handle.Lastpx.remote(req)
    #     print(result)
    #     return {"status ": 200}


    @app.post("/fi/test1")
    async def root(self, body: PostItem = Body(embed=True)):
        results = {"item": body.portfolioType, "aaa": body.portfolio}
        return results
        # return "hello"+ body.portfolioType

    @app.get("/fi/test2")
    async def root(self, body: Dict):
        print(123)
        print(body.values())
        return {"status ": 200}



lastpx_handle = LastpxService.bind()
side_handle = SideService.bind()
trddate_handle = TrddateService.bind()
volume_handle = VolumeService.bind()
yfinance_handle = YfinanceService.bind()
marginBalance_handle = MarginBalanceService.bind()
marketdataService_handle = MarketdataService.bind()
ingress = Finra.bind(lastpx_handle,side_handle,trddate_handle,volume_handle,yfinance_handle,marginBalance_handle,marketdataService_handle)
