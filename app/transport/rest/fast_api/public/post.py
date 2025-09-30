import uuid

from fastapi import FastAPI

from app.domain.models.post import POST_STATUS_ARCHIVE, POST_STATUS_DRAFT, POST_STATUS_PUBLIC
from app.transport.rest.fast_api.public.global_services import post_service


class PostApi:
    fastapi_app: FastAPI

    def __init__(self, app: FastAPI, api_prefix: str = "/post"):
        self.app = app
        self.api_prefix = api_prefix

    def register(self):
        self.app.post(self.api_prefix + "")(self.create)
        self.app.put(self.api_prefix + "")(self.publish)
        self.app.put(self.api_prefix + "")(self.archive)
        self.app.get(self.api_prefix + "/{id_}")(self.get)
        self.app.delete(self.api_prefix + "/{id_}")(self.delete)

    @staticmethod
    def create(
        title: str,
        body: str,
    ):
        return post_service.create_post(
            title=title,
            body=body,
            status=POST_STATUS_DRAFT,
        )

    @staticmethod
    def publish(id_: uuid.UUID):
        return post_service.update_post(id_, status=POST_STATUS_PUBLIC)

    @staticmethod
    def archive(id_: uuid.UUID):
        return post_service.update_post(id_, status=POST_STATUS_ARCHIVE)

    @staticmethod
    def get(id_: uuid.UUID):
        return post_service.get_post(id_)

    @staticmethod
    def delete(id_: uuid.UUID):
        return post_service.get_post(id_)

    @staticmethod
    def list_all():
        return post_service.list_posts()


# @public_api.post("/items")
# def create_item(name: str):
#     if not name or len(name) > 100:
#         raise ApiError(
#             code="validation_error", message="name must be 1..100 chars", status=422
#         )
#     item = {"id": len(_DB["items"]) + 1, "name": name}
#     _DB["items"].append(item)
#     return item
#
#
# @public_api.get("/items/{item_id}")
# def get_item(item_id: int):
#     for it in _DB["items"]:
#         if it["id"] == item_id:
#             return it
#     raise ApiError(code="not_found", message="item not found", status=404)
