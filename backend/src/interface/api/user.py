import hashlib
import hmac
import urllib.parse
from fastapi import APIRouter, Depends, File

from application.auth import get_user, get_userdata
from application.user import UserService
from config import MAX_AVATAR_SIZE, TG_TOKEN
from domain.user import FullUserDTO, BaseUser
from domain.user.models import PatchUser
from infrastructure.db import User, CTX_SESSION


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
    data: BaseUser = Depends(),
    userdata: dict = Depends(get_userdata)
) -> FullUserDTO:
    """
    Регистрация пользователя
    """
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

######################
#     TEST ONLY      #
######################

@router.post("/getauth")
async def getauth(id: int, username: str):
    data = f'user={{"id":{id},"first_name":"Zoom","last_name":"","username":"{username}","language_code":"en","allows_write_to_pm":true}}&chat_instance=6800930143016803379&chat_type=sender&auth_date=1729890471' # noqa E501
    tg = dict(urllib.parse.parse_qsl(urllib.parse.unquote(data)))
    params = "\n".join([f"{k}={v}" for k, v in sorted(tg.items(), key=lambda x: x[0])])
    hash = hmac.new(
        hmac.new("WebAppData".encode(), TG_TOKEN.encode(), hashlib.sha256).digest(),
        params.encode(),
        hashlib.sha256
    ).hexdigest()
    return urllib.parse.quote(data + "&hash=" + hash)
