from typing import AsyncGenerator
from fastapi import Depends, Security
from fastapi.security import APIKeyHeader
import hashlib
import hmac
import json
import asyncio
import urllib.parse

from config import TG_TOKEN
from domain.user import UserRepository
from application.user import UserService
from infrastructure.db import User, CTX_SESSION
from infrastructure.exc import AuthDataException, UnregisteredException


tg_auth = APIKeyHeader(name = "Tg-Authorization", description = "Telgram Init Data")

locks: dict[int, asyncio.Lock] = {}

async def get_userdata(auth: str = Security(tg_auth)) -> AsyncGenerator[dict, None]:
    tg = dict(urllib.parse.parse_qsl(urllib.parse.unquote(auth)))
    if not tg.get("hash"):
        raise AuthDataException
    hash = tg.pop('hash')
    params = "\n".join([f"{k}={v}" for k, v in sorted(tg.items(), key=lambda x: x[0])])
    truth_hash = hmac.new(
        hmac.new("WebAppData".encode(), TG_TOKEN.encode(), hashlib.sha256).digest(),
        params.encode(),
        hashlib.sha256
    ).hexdigest()
    if hash != truth_hash:
        raise AuthDataException

    user = json.loads(tg['user'])
    async with locks.setdefault(user['id'], asyncio.Lock()):
        yield user

async def get_userid(userdata: dict = Depends(get_userdata)) -> int:
    return userdata['id']

async def get_user(userdata: dict = Depends(get_userdata)) -> User:
    user = await UserRepository().get(userdata['id'])
    if not user:
        raise UnregisteredException

    username = userdata.get("username", None)
    try:
        await UserService().check_user(user, username)
    finally:
        await CTX_SESSION.get().commit()
    
    return user
