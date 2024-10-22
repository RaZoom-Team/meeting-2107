from fastapi import Depends, Request
import hashlib
import hmac
import json
import urllib.parse

from config import TG_TOKEN
from domain.user.repository import UserRepository
from infrastructure.db import User
from infrastructure.exc import AuthDataException
from infrastructure.exc.auth import UnregisteredException


async def get_userid(request: Request) -> int:
    tg = dict(urllib.parse.parse_qsl(request.headers.get("Tg-Authorization")))
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
    return user['id']

async def get_user(user_id: int = Depends(get_userid)) -> User:
    user = await UserRepository().get(user_id)
    if not user: raise UnregisteredException

    return user