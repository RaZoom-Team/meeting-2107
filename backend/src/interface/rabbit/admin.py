from faststream.rabbit import RabbitRouter

from application.user import UserService
from domain.user import BanUser, BannedUser, UserRepository
from infrastructure.db import CTX_SESSION


router = RabbitRouter(prefix="adm_")

@router.subscriber("ban")
@router.publisher("banned")
async def ban_user(data: BanUser) -> BannedUser:
    user = await UserRepository().get(data.user_id)
    if not user:
        return BannedUser(msg_id = data.msg_id, success = False)
    await UserService().ban(user, data.reason)
    await CTX_SESSION.get().commit()
    return BannedUser(msg_id = data.msg_id, success = True)