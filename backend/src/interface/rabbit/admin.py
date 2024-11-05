from faststream.rabbit import RabbitRouter

from application.tg.service import TelegramService
from application.user.rabbit import get_user
from application.user import UserService
from domain.user import UserRequest, BanUser, RabbitRequestResponse, GetUserResponse
from domain.user.models import VerifyUser
from infrastructure.db import CTX_SESSION


router = RabbitRouter(prefix="adm_")

@router.subscriber("ban")
async def ban_user(data: BanUser) -> RabbitRequestResponse:
    user = await get_user(data.user_id)
    if user.is_banned: return RabbitRequestResponse(success = False, error = "Пользователь уже заблокирован")
    await UserService().ban(user, data.reason)
    await CTX_SESSION.get().commit()
    return RabbitRequestResponse()

@router.subscriber("unban")
async def ban_user(data: UserRequest) -> RabbitRequestResponse:
    user = await get_user(data.user_id)
    if not user.is_banned: return RabbitRequestResponse(success = False, error = "Пользователь не заблокирован")
    await UserService().unban(user)
    await CTX_SESSION.get().commit()
    return RabbitRequestResponse()

@router.subscriber("verify")
async def verify_user(data: VerifyUser) -> RabbitRequestResponse:
    user = await get_user(data.user_id)
    if user.verify == data.value:
        return RabbitRequestResponse(success = False, error = "Пользователь уже верифицирован" if user.verify else "Пользовать не верифицирован")
    user.verify = data.value
    await CTX_SESSION.get().commit()
    await TelegramService().send_message(
        "✅ Ваш статус верификации был подтверждён администрацией" if user.verify else
        "⛔️ Ваш статус верификации был отозван администрацией",
        user.id
    )
    return RabbitRequestResponse()

@router.subscriber("user")
async def user(data: UserRequest) -> RabbitRequestResponse[GetUserResponse]:
    user = await get_user(data.user_id)
    return RabbitRequestResponse(
        response = GetUserResponse(
            text =
                f"<b>Имя:</b> {user.mention} <b>(<code>{user.id}</code>)</b>"
                f"\n<b>Класс:</b> {user.literal}"
                f"\n<b>Пол:</b> {'Мужской' if user.male else 'Женский'}"
                f"\n<b>Описание:</b> <i>{user.desc}</i>"
                f"\n<b>Верифицирован:</b> {'Да' if user.verify else 'Нет'}"
                f"\n<b>Заблокирован:</b> {f'Да ({user.ban_reason})' if user.is_banned else 'Нет'}",
            attachments = [attachment.url for attachment in user.attachments]
        )
    )