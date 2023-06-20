import json

import ray
import requests
from fastapi import Body, FastAPI
from typing import List, Dict
from ray import serve
from ray.serve.handle import RayServeDeploymentHandle
from ms.service.lastpx import LastpxService
from ms.service.compose_review import ComposeReviewService
from ms.service.upload_user_id import UploadUserIdService
from ms.service.upload_movie_id import UploadMovieIdService
from ms.service.mr_upload_text import MrUploadTextService
from ms.service.mr_upload_unique_id import MrUploadUniqueIdService
from ms.service.mr_compose_and_upload import MrComposeAndUploadService
from ms.service.store_review import StoreReviewService
from ms.service.upload_user_review import UploadUserReviewService
from ms.service.upload_movie_review import UploadMovieReviewService



app = FastAPI()


@serve.deployment()
@serve.ingress(app)
class MediaService:
    def __init__(
            self,
            lastpx_handle: RayServeDeploymentHandle,
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
        self._lastpx_handle = lastpx_handle
        self._compose_review_handle = compose_review_handle
        self._upload_user_id_handle = upload_user_id_handle
        self._upload_movie_id_handle = upload_movie_id_handle
        self._mr_upload_text_handle = mr_upload_text_handle
        self._mr_upload_unique_id_handle = mr_upload_unique_id_handle
        self._mr_compose_and_upload_handle = mr_compose_and_upload_handle
        self._store_review_service_handle = store_review_service_handle
        self._upload_user_review_handle = upload_user_review_handle
        self._upload_movie_review_handle = upload_movie_review_handle

    @app.post("/ms/lastpx")
    async def root1(self, body: Dict):
        result = await self._lastpx_handle.Lastpx.remote(body)
        r = json.dumps(await result)
        print(await result)
        return r

    @app.post("/ms/compose_review")
    async def root1(self, body: Dict):
        result = await self._compose_review_handle.ComposeReview.remote(body)
        r = json.dumps(await result)
        print(await result)
        return r

    @app.post("/ms/upload_user_id")
    async def root1(self, body: Dict):
        result = await self._upload_user_id_handle.UploadUserId.remote(body)
        r = json.dumps(await result)
        print(await result)
        return r

    @app.post("/ms/upload_movie_id")
    async def root1(self, body: Dict):
        result = await self._upload_movie_id_handle.UploadMovieId.remote(body)
        r = json.dumps(await result)
        print(await result)
        return r

    @app.post("/ms/upload_text")
    async def root1(self, body: Dict):
        result = await self._mr_upload_text_handle.MrUploadText.remote(body)
        r = json.dumps(await result)
        print(await result)
        return r

    @app.post("/ms/upload_unique_id")
    async def root1(self, body: Dict):
        result = await self._mr_upload_unique_id_handle.MrUploadUniqueId.remote(body)
        r = json.dumps(await result)
        print(await result)
        return r

    @app.post("/ms/mr_compose_and_upload")
    async def root1(self, body: List):
        result = await self._mr_compose_and_upload_handle.MrComposeAndUpload.remote(body)
        r = json.dumps(await result)
        print(await result)
        return r

    @app.post("/ms/store_review_service")
    async def root1(self, body: Dict):
        result = await self._store_review_service_handle.StoreReview.remote(body)
        r = json.dumps(await result)
        print(await result)
        return r

    @app.post("/ms/upload_user_review")
    async def root1(self, body: Dict):
        result = await self._upload_user_review_handle.UploadUserReview.remote(body)
        r = json.dumps(await result)
        print(await result)
        return r

    @app.post("/ms/upload_movie_review_handle")
    async def root1(self, body: Dict):
        result = await self._upload_movie_review_handle.UploadMovieReview.remote(body)
        r = json.dumps(await result)
        print(await result)
        return r

lastpx_handle = LastpxService.bind()
compose_review_handle = ComposeReviewService.bind()
upload_user_id_handle = UploadUserIdService.bind()
upload_movie_id_handle = UploadMovieIdService.bind()
mr_upload_text_handle = MrUploadTextService.bind()
mr_upload_unique_id_handle = MrUploadUniqueIdService.bind()
mr_compose_and_upload_handle = MrComposeAndUploadService.bind()
store_review_service_handle = StoreReviewService.bind()
upload_user_review_handle = UploadUserReviewService.bind()
upload_movie_review_handle = UploadMovieReviewService.bind()

ingress = MediaService.bind(lastpx_handle,compose_review_handle,upload_user_id_handle,upload_movie_id_handle,mr_upload_text_handle,mr_upload_unique_id_handle,mr_compose_and_upload_handle,store_review_service_handle,upload_user_review_handle,upload_movie_review_handle)
