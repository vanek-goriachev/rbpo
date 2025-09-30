from fastapi import FastAPI

from app.domain.services.post import PostService
from app.domain.services.post_tag import PostTagService
from app.transport.rest.fast_api.common.heathcheck import HealthCheckAPI
from app.transport.rest.fast_api.public.exception_handlers import PublicExceptionHandlers
from app.transport.rest.fast_api.public.post import PostApi
from app.transport.rest.fast_api.public.post_tag import PostTagApi


class PublicAPI:
    fastapi_app: FastAPI

    def __init__(
        self,
        fastapi_app: FastAPI,
        post_service: PostService,
        posts_tags_service: PostTagService,
    ) -> None:
        self.fastapi_app = fastapi_app

        self.exception_handlers = PublicExceptionHandlers(self.fastapi_app)

        self.healthcheck = HealthCheckAPI(self.fastapi_app, api_prefix="")
        self.post_api = PostApi(post_service, self.fastapi_app, api_prefix="/post")
        self.post_tag_api = PostTagApi(self.fastapi_app, api_prefix="/post_tag")

    def register(self):
        self.healthcheck.register()
        self.post_api.register()
        self.post_tag_api.register()
