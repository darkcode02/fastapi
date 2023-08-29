import typing
from starlette.middleware.base import BaseHTTPMiddleware, DispatchFunction, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response
from starlette.types import ASGIApp
from fastapi.responses import JSONResponse
from fastapi import FastAPI

class ErrorHandler(BaseHTTPMiddleware):
    def __init__(self, app: FastAPI )-> None:
        super().__init__(app)

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response or JSONResponse:
        try: 
            return await call_next(request)
        except Exception as e:
            return JSONResponse(status_code=500, content={'message':str(e)})