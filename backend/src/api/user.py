from fastapi import APIRouter, Depends, File

from application.auth import get_user, get_userid
from application.user import UserService
from config import MAX_AVATAR_SIZE
from domain.user import UserDTO, BaseUser
from infrastructure.db import User, CTX_SESSION


router = APIRouter(prefix="/user", tags=["User"])


@router.get("")
async def get_user_info(user: User = Depends(get_user)) -> UserDTO:
    """
    Получение информации о текущем пользователей
    """
    return user

@router.post(
    "",
    responses={
        403: {"description": "Already registered"},
        400: {"description": "Exceeded max file size (limit %s KB) / Invalid image file" % (MAX_AVATAR_SIZE / 1024)},
        401: {"description": "Invalid Telegram Data"}
    }
)
async def register_user(avatar: bytes = File(), data: BaseUser = Depends(), user_id: int = Depends(get_userid)) -> UserDTO:
    """
    Регистрация пользователя
    """
    user = await UserService().register(user_id, data, avatar)
    await CTX_SESSION.get().commit()
    return user