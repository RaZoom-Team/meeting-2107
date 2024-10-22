from contextlib import asynccontextmanager
from typing import Callable, Coroutine
from fastapi import FastAPI, APIRouter, Request
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.exc import IntegrityError, PendingRollbackError

from infrastructure.db import get_session
from infrastructure.db.session import CTX_SESSION

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
        401: {"description": "Invalid Telegram Data / This account is not registered"}
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

    @app.middleware("http")
    async def session_middleware(request: Request, coro):
        async with get_session() as session:
            CTX_SESSION.set(session)
            try:
                response = await coro(request)
            except (IntegrityError, PendingRollbackError) as err:
                await session.rollback()
                raise err
        return response

    return app