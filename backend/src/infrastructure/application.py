from contextlib import asynccontextmanager
from typing import Callable, Coroutine
from fastapi import FastAPI, APIRouter, Request
from starlette.middleware.cors import CORSMiddleware
from uvicorn.middleware.proxy_headers import ProxyHeadersMiddleware
# from logging_loki import LokiQueueHandler
# from multiprocessing import Queue
import logging

from src.config import IS_PROD, LOKI_URL, ROOT_PATH
from src.infrastructure.db import get_session, CTX_SESSION
from src.infrastructure.exc import HTTPError
# from src.infrastructure.utils import PrometheusMiddleware, metrics

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
        expose_headers = ["*"],
        allow_credentials = True
    )
    app.add_middleware(
        ProxyHeadersMiddleware,
        trusted_hosts = ["*"] # Direct access not allowed to API
    )

    # app.add_middleware(PrometheusMiddleware, app_name="mt2107", exclude_paths=["/metrics", "/system/ping"])
    # app.add_route("/metrics", metrics, include_in_schema=False)

    app.add_exception_handler(HTTPError, HTTPError.handler)

    logger = logging.getLogger("uvicorn.access")
    logger.addFilter(LoggingFilter(ignoring_log_endpoints))
    # if IS_PROD: 
    #     loki_logs_handler = LokiQueueHandler(
    #         Queue(-1),
    #         url=LOKI_URL,
    #         tags={"application": "mt2107"}
    #     )
    #     logger.addHandler(loki_logs_handler)

    logging.basicConfig(
        format = '[%(asctime)s.%(msecs)03dZ] %(name)s %(levelname)s %(message)s'
    )

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