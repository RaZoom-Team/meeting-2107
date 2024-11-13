from src.domain.user import UserRepository, RabbitRequestResponse
from src.infrastructure.rabbit import RabbitError
from src.infrastructure.db import User


async def get_user(user_id: int) -> User:
    user = await UserRepository().get(user_id)
    if not user:
        raise RabbitError(RabbitRequestResponse(success = False, error = "Пользователь не найден"))
    return user