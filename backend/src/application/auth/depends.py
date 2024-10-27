from fastapi import Depends, Header, Request, Security
import hashlib
import hmac
import json
import urllib.parse

from fastapi.security import APIKeyHeader

from config import TG_TOKEN
from domain.user.repository import UserRepository
from infrastructure.db import User
from infrastructure.db.session import CTX_SESSION
from infrastructure.exc import AuthDataException
from infrastructure.exc.auth import UnregisteredException, UsernameRequired


tg_auth = APIKeyHeader(name = "Tg-Authorization", description = "Telgram Init Data")

async def get_userdata(auth: str = Security(tg_auth)) -> dict:
    tg = dict(urllib.parse.parse_qsl(urllib.parse.unquote(auth)))
    if not tg.get("hash"): raise AuthDataException
    hash = tg.pop('hash')
    params = "\n".join([f"{k}={v}" for k, v in sorted(tg.items(), key=lambda x: x[0])])
    truth_hash = hmac.new(
        hmac.new("WebAppData".encode(), TG_TOKEN.encode(), hashlib.sha256).digest(),
        params.encode(),
        hashlib.sha256
    ).hexdigest()
    if hash != truth_hash: raise AuthDataException

    user = json.loads(tg['user'])
    return user

async def get_userid(userdata: dict = Depends(get_userdata)) -> int:
    return userdata['id']

async def get_user(userdata: dict = Depends(get_userdata)) -> User:
    user = await UserRepository().get(userdata['id'])
    if not user: raise UnregisteredException

    username = userdata.get("username", None)
    if not username:
        user.is_active = False
        await CTX_SESSION.get().commit()
        raise UsernameRequired
    if user.username != username:
        user.username = username
        await CTX_SESSION.get().commit()
    return user