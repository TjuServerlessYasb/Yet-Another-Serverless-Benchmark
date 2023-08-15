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
import asyncio
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
    async def lastpx(self, body: Dict):
        result = await self._lastpx_handle.Lastpx.remote(body)
        return result


    @app.post("/fi/side")
    async def side(self, body: Dict):
        result = await self._side_handle.Side.remote(body)
        return result

    @app.post("/fi/trddate")
    async def trddate(self, body: Dict):
        result = await self._trddate_handle.Trddate.remote(body)
        return result

    @app.post("/fi/volume")
    async def volume(self, body: Dict):
        result = await self._volume_handle.Volume.remote(body)
        return result

    @app.post("/fi/yfinance")
    async def yfinance(self, body: Dict):
        result = await self._yfinance_handle.Yfinance.remote(body)
        r = json.dumps(await result)
        print(await result)
        return r


    # @app.post("/fi/volume")
    # async def volume(self, body: Dict):
    #     result = await self._volume_handle.Volume.remote(body)
    #     return result

    @app.post("/fi/marginBalance")
    async def marginBalance(self, dic: List):
        result = await self._marginBalance_handle.MarginBalance.remote(dic)
        return result

    @app.post("/fi/marketdata")
    async def marketdata(self, dic: Dict):
        result = await self._marketdataService_handle.Marketdata.remote(dic)
        return result

    @app.get("/fi/workflow")
    async def root(self):
        try:
            # curl http://10.244.0.183:8000/fi/workflow
            print(123132123)
            req = {"body": {"portfolioType": "S&P", "portfolio": "1234"}}
            tasks = []
            task = asyncio.ensure_future(self.marketdata(req))
            tasks.append(task)
            task = asyncio.ensure_future(self.lastpx(req))
            tasks.append(task)
            task = asyncio.ensure_future(self.side(req))
            tasks.append(task)
            task = asyncio.ensure_future(self.trddate(req))
            tasks.append(task)
            task = asyncio.ensure_future(self.volume(req))
            tasks.append(task)

            res = await asyncio.gather(*tasks)
            print(res)
            for i in res:
                print(type(i))
                print(i)

            result = await self.marginBalance(res)
            print("marginBalance result")
            print(result)






        except Exception as e:
            print(e)
            print(e.__traceback__.tb_frame.f_globals["__file__"])  # 发生异常所在的文件
            print(e.__traceback__.tb_lineno)  # 发生异常所在的行数
        else:
            print("success")
        return {"message": 200, "result": 1}



lastpx_handle = LastpxService.bind()
side_handle = SideService.bind()
trddate_handle = TrddateService.bind()
volume_handle = VolumeService.bind()
yfinance_handle = YfinanceService.bind()
marginBalance_handle = MarginBalanceService.bind()
marketdataService_handle = MarketdataService.bind()
ingress = Finra.bind(lastpx_handle,side_handle,trddate_handle,volume_handle,yfinance_handle,marginBalance_handle,marketdataService_handle)
