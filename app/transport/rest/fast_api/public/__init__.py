from fastapi import FastAPI

from app.domain.services.post import PostService
from app.domain.services.post_tag import PostTagService
from app.transport.rest.fast_api.common.heathcheck import HealthCheckAPI
from app.transport.rest.fast_api.public.exception_handlers import PublicExceptionHandlers
from app.transport.rest.fast_api.public.global_services import initialize
from app.transport.rest.fast_api.public.post import PostApi
from app.transport.rest.fast_api.public.post_tag import PostTagApi


class PublicAPI:
    fastapi_app: FastAPI

    def __init__(self, fastapi_app: FastAPI) -> None:
        self.fastapi_app = fastapi_app

        self.exception_handlers = PublicExceptionHandlers(self.fastapi_app)

        self.healthcheck = HealthCheckAPI(self.fastapi_app, api_prefix="")
        self.post_api = PostApi(self.fastapi_app, api_prefix="/post")
        self.post_tag_api = PostTagApi(self.fastapi_app, api_prefix="/post_tag")

    @staticmethod
    def set_domain_services(post_service: PostService, post_tag_service: PostTagService):
        initialize(post_service, post_tag_service)

    def register(self):
        self.healthcheck.register()
        self.post_api.register()
        self.post_tag_api.register()
