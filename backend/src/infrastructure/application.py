from contextlib import asynccontextmanager
from typing import Callable, Coroutine
from fastapi import FastAPI, APIRouter, Request
from starlette.middleware.cors import CORSMiddleware
from uvicorn.middleware.proxy_headers import ProxyHeadersMiddleware
import logging

from config import ROOT_PATH
from infrastructure.db import get_session, CTX_SESSION
from infrastructure.exc import HTTPError

def create_app(
        routers: list[APIRouter],
        startup_tasks: list[Callable[[], Coroutine]] = [],
        shutdown_tasks: list[Callable[[], Coroutine]] = [],
        ignoring_log_endpoints: list[tuple[str, str]] = [], # tuple[endpoint_path, method]
        root_path: str = ""
    ):

    @asynccontextmanager
    async def lifespan(app: FastAPI):
        for task in startup_tasks:
            await task()
        yield
        for task in shutdown_tasks:
            await task()

    app = FastAPI(
        title = "Meeting 2107",
        lifespan = lifespan,
        responses = {
            400: {"description": "Invalid Telegram Data (2000)"},
            401: {"description": "This account is not registered (3000) / Username required (2001)"},
            403: {"description": "Subscription to channel required (3004) / Your account has been banned (3005)"}
        }, 
        root_path = root_path
    )

    for router in routers:
        app.include_router(router)
    
    app.add_middleware(
        CORSMiddleware,
        allow_origins = ["*"],
        allow_methods = ["*"],
        allow_headers = ["*"],
        allow_credentials = True
    )
    app.add_middleware(
        ProxyHeadersMiddleware,
        trusted_hosts = ["*"] # Direct access not allowed to API
    )
    app.add_exception_handler(HTTPError, HTTPError.handler)

    logging.getLogger("uvicorn.access").addFilter(LoggingFilter(ignoring_log_endpoints))

    @app.middleware("http")
    async def session_middleware(request: Request, coro):
        async with get_session() as session:
            CTX_SESSION.set(session)
            response = await coro(request)
        return response

    return app

class LoggingFilter(logging.Filter):
    def __init__(self, ignoring_log_endpoints: list[tuple[str, str]]) -> None:
        super().__init__()
        self.ignoring_log_endpoints = ignoring_log_endpoints

    def filter(self, record: logging.LogRecord) -> bool:
        for endpoint, method in self.ignoring_log_endpoints:
            if f"{method.upper()} {endpoint}" in record.getMessage().replace(ROOT_PATH, "", 1):
                return False
        return True