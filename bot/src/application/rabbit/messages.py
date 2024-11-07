from typing import Literal
from models import ReasonRequest, RequestResponse, GetUserResponse, GetUsers, GetUsersResponse, UserRequest, VerifyUser
from .rpc import send_rpc


async def ban_user(user_id: int, reason: str) -> RequestResponse:
    return await send_rpc(
        ReasonRequest(user_id = user_id, reason = reason),
        "adm_ban"
    )

async def unban_user(user_id: int) -> RequestResponse:
    return await send_rpc(
        UserRequest(user_id = user_id),
        "adm_unban"
    )

async def verify_user(user_id: int, value: bool) -> RequestResponse:
    return await send_rpc(
        VerifyUser(user_id = user_id, value = value),
        "adm_verify"
    )

async def get_user(user_id: int) -> RequestResponse[GetUserResponse]:
    return await send_rpc(
        UserRequest(user_id = user_id),
        "adm_user",
        GetUserResponse
    )

async def get_users(offset: int, limit: int = 25, filter: Literal["all", "banned", "verify"] = "all") -> RequestResponse[GetUsersResponse]:
    return await send_rpc(
        GetUsers(offset = offset, limit = limit, filter = filter),
        "adm_users",
        GetUsersResponse
    )