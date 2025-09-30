from fastapi import FastAPI


class HealthCheckAPI:
    fastapi_app: FastAPI

    def __init__(self, fastapi_app: FastAPI, api_prefix: str = ""):
        self.fastapi_app = fastapi_app
        self.api_prefix = api_prefix

    def register(self):
        self.fastapi_app.get(self.api_prefix + "/health")(self.health)

    @staticmethod
    def health():
        return {"status": "ok"}
