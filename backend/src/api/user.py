from fastapi import APIRouter, Depends, File

from application.auth import get_user, get_userid
from application.user import UserService
from config import MAX_AVATAR_SIZE
from domain.user import UserDTO, BaseUser
from infrastructure.db import User, CTX_SESSION


router = APIRouter(prefix="/user")

@router.get("")
async def get_user_info(user: User = Depends(get_user)) -> UserDTO:
    """
    Получение информации о текущем пользователей
    """
    return UserDTO(
        name = user.name,
        surname = user.surname,
        desc = user.desc,
        literal = user.literal,
        male = user.male,
        is_active = user.is_active
    )

@router.post(
    "",
    responses={
        403: {"description": "Already registered"},
        400: {"description": "Exceeded max file size (limit %s KB) / Invalid image file" % (MAX_AVATAR_SIZE / 1024)}
    }
)
async def register_user(avatar: bytes = File(), data: BaseUser = Depends(), user_id: int = Depends(get_userid)) -> UserDTO:
    """
    Регистрация пользователя
    """
    user = await UserService().register(user_id, data, avatar)
    await CTX_SESSION.get().commit()
    return UserDTO(
        name = user.name,
        surname = user.surname,
        desc = user.desc,
        literal = user.literal,
        male = user.male,
        is_active = user.is_active
    )