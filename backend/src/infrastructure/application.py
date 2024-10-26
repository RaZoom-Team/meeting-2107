from contextlib import asynccontextmanager
from typing import Callable, Coroutine
from fastapi import FastAPI, APIRouter, Request
from fastapi.middleware.cors import CORSMiddleware

from infrastructure.db import get_session, CTX_SESSION
from infrastructure.exc import HTTPError

def create_app(
        routers: list[APIRouter],
        startup_tasks: list[Callable[[], Coroutine]] = [],
        shutdown_tasks: list[Callable[[], Coroutine]] = []
    ):

    @asynccontextmanager
    async def lifespan(app: FastAPI):
        for task in startup_tasks:
            await task()
        yield
        for task in shutdown_tasks:
            await task()

    app = FastAPI(lifespan=lifespan, responses = {
        400: {"description": "Invalid Telegram Data (2000)"},
        401: {"description": "This account is not registered (3000) / Username required (2001)"}
    })

    for router in routers:
        app.include_router(router)
    
    app.add_middleware(
        CORSMiddleware,
        allow_origins = ["*"],
        allow_methods = ["*"],
        allow_headers = ["*"],
        allow_credentials = True
    )
    app.add_exception_handler(HTTPError, HTTPError.handler)

    @app.middleware("http")
    async def session_middleware(request: Request, coro):
        async with get_session() as session:
            CTX_SESSION.set(session)
            response = await coro(request)
        return response

    return app