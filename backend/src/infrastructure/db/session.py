from contextvars import ContextVar
from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    create_async_engine
)

from config import DB_URL

engine: AsyncEngine = create_async_engine(DB_URL, pool_size = 100, max_overflow = 0)

async def init_models():
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

def get_session():
    session = AsyncSession(engine, expire_on_commit=False, autoflush=False)
    return session

CTX_SESSION: ContextVar[AsyncSession] = ContextVar("CTX_SESSION")