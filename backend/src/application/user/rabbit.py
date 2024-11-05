from domain.user import UserRepository, RabbitRequestResponse
from infrastructure.rabbit import RabbitError
from infrastructure.db import User


async def get_user(user_id: int) -> User:
    user = await UserRepository().get(user_id)
    if not user:
        raise RabbitError(RabbitRequestResponse(success = False, error = "Пользователь не найден"))
    return user