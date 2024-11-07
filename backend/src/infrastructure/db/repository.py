from abc import ABC
from sqlmodel import SQLModel, select, func

from .session import CTX_SESSION

class BaseRepository[T: SQLModel](ABC):

    def __init__(self) -> None:
        self.session = CTX_SESSION.get()

    async def get(self, **kwargs) -> SQLModel | None:
        raise NotImplementedError
    
    async def insert(self, **kwargs) -> SQLModel:
        raise NotImplementedError
    
    async def delete(self, obj: T) -> None:
        await self.session.delete(obj)
        await self.session.flush()