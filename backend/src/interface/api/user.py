import hashlib
import hmac
import urllib.parse
from fastapi import APIRouter, Depends, File, HTTPException

from src.infrastructure.utils import to_form
from src.application.auth import get_user, get_userdata
from src.application.user import UserService
from src.config import MAX_AVATAR_SIZE, TG_TOKEN
from src.domain.user import FullUserDTO, BaseUser, PatchUser
from src.infrastructure.db import User, CTX_SESSION


router = APIRouter(prefix="/user", tags=["User"])


@router.get("")
async def get_user_info(user: User = Depends(get_user)) -> FullUserDTO:
    """
    Получение информации о текущем пользователе
    """
    try:
        await UserService().check_user_subcription(user)
    finally:
        await CTX_SESSION.get().commit()
    return user

@router.post(
    "",
    responses={
        400: {
            "description": "Exceeded max file size (limit %s KB) (2002) / Invalid image file (2003)"
            % (MAX_AVATAR_SIZE / 1024)
        },
        401: {"description": "Username required (2001)"},
        403: {"description": "Already registered (3001) / Subscription to channel required (3004) / Your account has been banned (3005)"}
    }
)
async def register_user(
    avatar: bytes = File(),
    data: BaseUser = Depends(to_form(BaseUser)),
    userdata: dict = Depends(get_userdata)
) -> FullUserDTO:
    """
    Регистрация пользователя
    """
    data.name, data.surname = data.name.strip(), data.surname.strip()
    if " " in data.name or " " in data.surname:
        raise HTTPException(422, "name and surname should be one word")
    user = await UserService().register(userdata, data, avatar)
    await CTX_SESSION.get().commit()
    return user


@router.patch("")
async def edit_user(data: PatchUser, user: User = Depends(get_user)) -> FullUserDTO:
    """
    Редактирование пользователя
    """
    await UserService().edit_user(user, data)
    await CTX_SESSION.get().commit()
    return user


@router.patch(
    "/avatar",
    responses={
        400: {
            "description": "Exceeded max file size (limit %s KB) (2002) / Invalid image file (2003)"
            % (MAX_AVATAR_SIZE / 1024)
        },
    }
)
async def update_avatar(avatar: bytes = File(), user: User = Depends(get_user)) -> FullUserDTO:
    """
    Обновление аватара пользователя
    """
    await UserService().update_avatar(user, avatar)
    await CTX_SESSION.get().commit()
    return user

@router.post(
    "/verify",
    responses={
        403: {"description": "You already verified (3006)"}
    }
)
async def send_verify(user: User = Depends(get_user)) -> FullUserDTO:
    await UserService().send_verify_request(user)
    return user