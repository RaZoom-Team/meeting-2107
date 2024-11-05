from dataclasses import dataclass
from typing import Callable, Dict, Awaitable, Any
from aiogram import BaseMiddleware
from aiogram.types import Message
from pydantic import BaseModel
import inspect


class ValidatingMiddleware(BaseMiddleware):

    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any]
    ) -> Any:
        param = inspect.signature(data['handler'].callback).parameters.get("data", None)
        if param:
            model = param.annotation
            args = event.text.split()[1:]
            assert issubclass(model, BaseModel), "Invalid data model"
            assert isinstance(param.default, Data), "Invalid data type"
            try:
                data['data'] = model(**{
                    k.replace(":", "", 1): (' '.join(args[i:]) if k.startswith(":") else args[i])
                    for i, k in enumerate(param.default.order)
                    if len(args) - 1 >= i
                })
            except ValueError:
                return await event.reply(param.default.error)
        return await handler(event, data)
    
@dataclass
class Data:
    order: list[str]
    error: str