from abc import ABC
from sqlmodel import SQLModel, select, insert

from .session import CTX_SESSION

class BaseRepository(ABC):

    def __init__(self) -> None:
        self.session = CTX_SESSION.get()

    async def get(self, **kwargs) -> SQLModel | None:
        raise NotImplementedError
    
    # @abstractmethod
    # async def update(self, **kwargs) -> None:
    #     raise NotImplementedError
    
    async def insert(self, **kwargs) -> SQLModel:
        raise NotImplementedError
    
    async def delete(self, **kwargs) -> None:
        raise NotImplementedError

# class PrimaryRepository[T: SQLModel, PK: int | str](BaseRepository):
#     _table: type[T]
#     _primary_key: str

#     async def get(self, id: PK) -> T | None:
#         query = select(self._table).where(getattr(self._table, self._primary_key))
#         record = await self.session.exec(query)
#         return record.first()

#     async def insert(self, obj: T) -> T:
#         self.session.add(T)
#         await self.session.refresh(obj)
#         return obj
    
#     async def delete(self, id: PK)

# class PrimaryRepository(BaseRepository[MT, Table]):

#     primary: str

#     async def get(self, id: int | str, **kwargs) -> Optional[MT]:
#         return await self._get_one(getattr(self.schema_class, self.primary) == id, **kwargs)
    
#     async def update(self, id: int | str, **payload):
#         await self._update(getattr(self.schema_class, self.primary) == id, **payload)

#     async def update_many(self, ids: list[int | str], **payload):
#         await self._update(getattr(self.schema_class, self.primary).in_(ids), **payload)

#     async def delete(self, id: int | str):
#         await self._delete(getattr(self.schema_class, self.primary) == id)

#     async def count(self, expression: ColumnExpressionArgument) -> int:
#         return self._get_count(expression)

#     async def get_all(self, **kwargs) -> list[MT]:
#         return await self._get_all(**kwargs)