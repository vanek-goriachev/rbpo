import uuid

from fastapi import FastAPI, Request

from app.domain.models.post import POST_STATUS_ARCHIVE, POST_STATUS_DRAFT, POST_STATUS_PUBLIC
from app.domain.services.post import PostService


class PostApi:
    fastapi_app: FastAPI

    def __init__(self, post_service: PostService, app: FastAPI, api_prefix: str = "/post"):
        self.post_service = post_service
        self.app = app
        self.api_prefix = api_prefix

    def register(self):
        self.app.post(self.api_prefix + "")(self.create())
        self.app.get(self.api_prefix + "")(self.list_all())
        self.app.get(self.api_prefix + "/{id_}")(self.get())
        self.app.put(self.api_prefix + "/{id_}/publish")(self.publish())
        self.app.put(self.api_prefix + "/{id_}/archive")(self.archive())
        self.app.delete(self.api_prefix + "/{id_}")(self.delete())

    def create(self):

        async def f(request: Request):
            body = await request.json()

            return self.post_service.create_post(
                title=body.get("title"),
                body=body.get("body"),
                status=POST_STATUS_DRAFT,
            )

        return f

    def publish(self):

        def f(id_: uuid.UUID):
            return self.post_service.update_post(id_, status=POST_STATUS_PUBLIC)

        return f

    def archive(self):

        def f(id_: uuid.UUID):
            return self.post_service.update_post(id_, status=POST_STATUS_ARCHIVE)

        return f

    def get(self):

        def f(id_: uuid.UUID):
            return self.post_service.get_post(id_)

        return f

    def delete(self):

        def f(id_: uuid.UUID):
            return self.post_service.delete_post(id_)

        return f

    def list_all(self):

        def f():
            return self.post_service.list_posts()

        return f
