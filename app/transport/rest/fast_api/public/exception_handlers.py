from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse

from app.domain.models.errors.domain import DomainError, NotFoundError
from app.transport.rest.fast_api.common.errors import ApiError


class PublicExceptionHandlers:
    fastapi_app: FastAPI

    def __init__(self, fastapi_app: FastAPI):
        self.fastapi_app = fastapi_app

    def register(self):
        self.fastapi_app.exception_handler(ApiError)(self.api_error_handler)
        self.fastapi_app.exception_handler(HTTPException)(self.http_exception_handler)
        self.fastapi_app.exception_handler(DomainError)(self.domain_error_handler)

    @staticmethod
    async def domain_error_handler(request: Request, error: DomainError) -> JSONResponse:
        if isinstance(error, NotFoundError):
            return JSONResponse(status_code=404, content={"error": {"code": "not_found"}})

        return JSONResponse(
            status_code=400,
            content={"error": error.message},
        )

    @staticmethod
    async def api_error_handler(request: Request, exc: ApiError):
        return JSONResponse(
            status_code=exc.status,
            content={"error": {"code": exc.code, "message": exc.message}},
        )

    @staticmethod
    async def http_exception_handler(request: Request, exc: HTTPException):
        # Normalize FastAPI HTTPException into our error envelope
        detail = exc.detail if isinstance(exc.detail, str) else "http_error"
        return JSONResponse(
            status_code=exc.status_code,
            content={"error": {"code": "http_error", "message": detail}},
        )
