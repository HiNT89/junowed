from uuid import uuid4

from fastapi import Request
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse


class APIError(Exception):
    def __init__(self, status_code: int, code: str, message: str, details: dict | None = None):
        self.status_code = status_code
        self.code = code
        self.message = message
        self.details = details


async def api_error_handler(_: Request, exc: APIError) -> JSONResponse:
    error: dict = {"code": exc.code, "message": exc.message, "requestId": str(uuid4())}
    if exc.details:
        error["details"] = exc.details
    return JSONResponse(status_code=exc.status_code, content={"error": error})


async def validation_error_handler(_: Request, exc: RequestValidationError) -> JSONResponse:
    return JSONResponse(
        status_code=422,
        content={
            "error": {
                "code": "INVALID_CONFIG",
                "message": "Request validation failed",
                "requestId": str(uuid4()),
                "details": {"issues": jsonable_encoder(exc.errors())},
            }
        },
    )
