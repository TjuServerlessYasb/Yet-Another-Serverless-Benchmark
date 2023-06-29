import json
import ray
import requests
from fastapi import Body, FastAPI
from typing import List, Dict
from ray import serve
from ray.serve.handle import RayServeDeploymentHandle
from ms.service.compose_review import ComposeReviewService
from ms.service.upload_user_id import UploadUserIdService
from ms.service.upload_movie_id import UploadMovieIdService
from ms.service.mr_upload_text import MrUploadTextService
from ms.service.mr_upload_unique_id import MrUploadUniqueIdService
from ms.service.mr_compose_and_upload import MrComposeAndUploadService
from ms.service.store_review import StoreReviewService
from ms.service.upload_user_review import UploadUserReviewService
from ms.service.upload_movie_review import UploadMovieReviewService
import asyncio
import random
import string
import time

app = FastAPI()

def gen_random_string(i):
    choices = string.ascii_letters + string.digits
    return "".join([choices[random.randint(0, len(choices)-1)] for j in range(i)])

movie_titles = []
with open("movie_titles.csv", "r") as f:
    movie_titles = f.readlines()

def generate_data():
    user_index = str(random.randint(1, 1000))
    review = {
        "username": "username_" + user_index,
        "password": "password_" + user_index,
        "title": movie_titles[random.randint(0, len(movie_titles)-1)].strip(),
        "rating": random.randint(0, 10),
        "text": gen_random_string(256)
    }
    return review


@serve.deployment()
@serve.ingress(app)
class MediaService:
    def __init__(
            self,
            compose_review_handle: RayServeDeploymentHandle,
            upload_user_id_handle: RayServeDeploymentHandle,
            upload_movie_id_handle: RayServeDeploymentHandle,
            mr_upload_text_handle: RayServeDeploymentHandle,
            mr_upload_unique_id_handle: RayServeDeploymentHandle,
            mr_compose_and_upload_handle: RayServeDeploymentHandle,
            store_review_service_handle: RayServeDeploymentHandle,
            upload_user_review_handle: RayServeDeploymentHandle,
            upload_movie_review_handle: RayServeDeploymentHandle,

    ):
        self._compose_review_handle = compose_review_handle
        self._upload_user_id_handle = upload_user_id_handle
        self._upload_movie_id_handle = upload_movie_id_handle
        self._mr_upload_text_handle = mr_upload_text_handle
        self._mr_upload_unique_id_handle = mr_upload_unique_id_handle
        self._mr_compose_and_upload_handle = mr_compose_and_upload_handle
        self._store_review_service_handle = store_review_service_handle
        self._upload_user_review_handle = upload_user_review_handle
        self._upload_movie_review_handle = upload_movie_review_handle


    @app.post("/ms/compose_review")
    async def compose_review(self, body: Dict):
        result = await self._compose_review_handle.ComposeReview.remote(body)
        # r = json.dumps(await result)
        # print(await result)
        return result

    @app.post("/ms/upload_user_id")
    async def upload_user_id(self, body: Dict):
        result = await self._upload_user_id_handle.UploadUserId.remote(body)

        return result

    @app.post("/ms/upload_movie_id")
    async def upload_movie_id(self, body: Dict):
        result = await self._upload_movie_id_handle.UploadMovieId.remote(body)
        # r = json.dumps(await result)
        # print(await result)
        return result

    @app.post("/ms/upload_text")
    async def upload_text(self, body: Dict):
        result = await self._mr_upload_text_handle.MrUploadText.remote(body)
        # r = json.dumps(await result)
        # print(await result)
        return result

    @app.post("/ms/upload_unique_id")
    async def upload_unique_id(self, body: Dict):
        result = await self._mr_upload_unique_id_handle.MrUploadUniqueId.remote(body)
        # r = json.dumps(await result)
        # print(await result)
        return result

    @app.post("/ms/mr_compose_and_upload")
    async def mr_compose_and_upload(self, body: List):
        result = await self._mr_compose_and_upload_handle.MrComposeAndUpload.remote(body)
        # r = json.dumps(await result)
        # print(await result)
        return result

    @app.post("/ms/store_review_service")
    async def store_review(self, body: Dict):
        result = await self._store_review_service_handle.StoreReview.remote(body)

        return result

    @app.post("/ms/upload_user_review")
    async def upload_user_review(self, body: Dict):
        result = await self._upload_user_review_handle.UploadUserReview.remote(body)

        return result

    @app.post("/ms/upload_movie_review_handle")
    async def upload_movie_review(self, body: Dict):
        result = await self._upload_movie_review_handle.UploadMovieReview.remote(body)

        return result

    @app.get("/ms/workflow")
    async def root(self):
        try:
            # curl http://10.244.0.183:8000/ms/workflow
            review = generate_data()
            start = time.time()
            compose_res = await self.compose_review(review)

            print(await compose_res)

            # compose_dict = {"compose_res":compose_res}

            tasks = []
            task = asyncio.ensure_future(self.upload_movie_id(await compose_res))
            tasks.append(task)
            task = asyncio.ensure_future(self.upload_text(await compose_res))
            tasks.append(task)
            task = asyncio.ensure_future(self.upload_unique_id(await compose_res))
            tasks.append(task)
            task = asyncio.ensure_future(self.upload_user_id(await compose_res))
            tasks.append(task)

            res = await asyncio.gather(*tasks)
            print("4 result")
            for i in res:
                print(i)
                print(type(i))
                print(ray.get(ray.get(i)))

            compose_and_upload_res = await self.mr_compose_and_upload(res)
            print(await compose_and_upload_res)

            tasks = []
            task = asyncio.ensure_future(self.store_review(await compose_and_upload_res))
            tasks.append(task)
            task = asyncio.ensure_future(self.upload_user_review(await compose_and_upload_res))
            tasks.append(task)
            task = asyncio.ensure_future(self.upload_movie_review(await compose_and_upload_res))
            tasks.append(task)

            res = await asyncio.gather(*tasks)
            print("3 function:")
            result = {}
            for i in res:
                print(i)
                print(ray.get(i))
                result.update(ray.get(i))

            print(result)





        except Exception as e:
            print(e)
            print(e.__traceback__.tb_frame.f_globals["__file__"])  # 发生异常所在的文件
            print(e.__traceback__.tb_lineno)  # 发生异常所在的行数
        else:
            print("success")
        return {"message": 200, "result": result}


compose_review_handle = ComposeReviewService.bind()
upload_user_id_handle = UploadUserIdService.bind()
upload_movie_id_handle = UploadMovieIdService.bind()
mr_upload_text_handle = MrUploadTextService.bind()
mr_upload_unique_id_handle = MrUploadUniqueIdService.bind()
mr_compose_and_upload_handle = MrComposeAndUploadService.bind()
store_review_service_handle = StoreReviewService.bind()
upload_user_review_handle = UploadUserReviewService.bind()
upload_movie_review_handle = UploadMovieReviewService.bind()

ingress = MediaService.bind(compose_review_handle,upload_user_id_handle,upload_movie_id_handle,mr_upload_text_handle,mr_upload_unique_id_handle,mr_compose_and_upload_handle,store_review_service_handle,upload_user_review_handle,upload_movie_review_handle)
