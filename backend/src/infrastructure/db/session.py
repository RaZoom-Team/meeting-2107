from contextvars import ContextVar
from sqlalchemy import text
from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    create_async_engine
)

from src.config import DB_URL

engine: AsyncEngine = create_async_engine(DB_URL, pool_size = 200, max_overflow = 0, pool_recycle=600)

# async def init_models():
#     async with engine.begin() as conn:
#         await conn.run_sync(SQLModel.metadata.create_all)

def get_session():
    session = AsyncSession(engine, expire_on_commit=False, autoflush=False)
    return session

async def ping_db() -> None:
    await CTX_SESSION.get().exec(text("SELECT 1"))

CTX_SESSION: ContextVar[AsyncSession] = ContextVar("CTX_SESSION")