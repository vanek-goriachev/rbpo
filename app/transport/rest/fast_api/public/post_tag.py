from fastapi import FastAPI


class PostTagApi:
    fastapi_app: FastAPI

    def __init__(self, fastapi_app: FastAPI, api_prefix: str = "post_tag"):
        self.fastapi_app = fastapi_app

    def register(self):
        pass
