from faststream.rabbit import RabbitRouter

from application.user import UserService
from domain.user import BanUser, VerifyUser, UnbanUser, GetUser, TelegramRequestResponse, GetUserResponse, UserRepository
from infrastructure.db import CTX_SESSION


router = RabbitRouter(prefix="adm_")

@router.subscriber("ban")
@router.publisher("banned")
async def ban_user(data: BanUser) -> TelegramRequestResponse:
    user = await UserRepository().get(data.user_id)
    if not user:
        return TelegramRequestResponse(msg_id = data.msg_id, success = False)
    await UserService().ban(user, data.reason)
    await CTX_SESSION.get().commit()
    return TelegramRequestResponse(msg_id = data.msg_id, success = True)

@router.subscriber("unban")
@router.publisher("unbanned")
async def ban_user(data: UnbanUser) -> TelegramRequestResponse:
    user = await UserRepository().get(data.user_id)
    if not user:
        return TelegramRequestResponse(msg_id = data.msg_id, success = False)
    await UserService().unban(user)
    await CTX_SESSION.get().commit()
    return TelegramRequestResponse(msg_id = data.msg_id, success = True)

@router.subscriber("verify")
@router.publisher("verified")
async def ban_user(data: VerifyUser) -> TelegramRequestResponse:
    user = await UserRepository().get(data.user_id)
    if not user:
        return TelegramRequestResponse(msg_id = data.msg_id, success = False)
    user.verify = data.value
    await CTX_SESSION.get().commit()
    return TelegramRequestResponse(msg_id = data.msg_id, success = True)

@router.subscriber("user")
@router.publisher("user-res")
async def ban_user(data: GetUser) -> GetUserResponse:
    user = await UserRepository().get(data.user_id)
    if not user:
        return GetUserResponse(msg_id = data.msg_id, success = False, text = "", attachments = [])
    return GetUserResponse(
        text =
            f"<b>Имя:</b> {user.mention} <b>(<code>{user.id}</code>)</b>"
            f"\n<b>Класс:</b> {user.literal}"
            f"\n<b>Пол:</b> {'Мужской' if user.male else 'Женский'}"
            f"\n<b>Описание:</b> <i>{user.desc}</i>"
            f"\n<b>Верифицирован:</b> {'Да' if user.verify else 'Нет'}"
            f"\n<b>Заблокирован:</b> {f'Да ({user.ban_reason})' if user.is_banned else 'Нет'}",
        msg_id = data.msg_id,
        attachments = [attachment.url for attachment in user.attachments],
        success = True
    )