from faststream.rabbit import RabbitRouter
import math

from src.application.tg.service import TelegramService
from src.application.user.rabbit import get_user
from src.application.user import UserService
from src.domain.user import UserRequest, BanUser, RabbitRequestResponse, GetUserResponse, GetUsers, VerifyUser, GetUsersResponse
from src.domain.user.repository import UserRepository
from src.infrastructure.db import CTX_SESSION
from src.infrastructure.db.tables import User


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
                f"<b>Имя:</b> {user.mention} <b>(<code>{user.id}</code>)</b> {'[НЕАКТИВЕН]' if not user.is_active else ''}"
                f"\n<b>Класс:</b> {user.literal}"
                f"\n<b>Пол:</b> {'Мужской' if user.male else 'Женский'}"
                f"\n<b>Описание:</b> <i>{user.desc}</i>"
                f"\n<b>Верифицирован:</b> {'Да' if user.verify else 'Нет'}"
                f"\n<b>Заблокирован:</b> {f'Да ({user.ban_reason})' if user.is_banned else 'Нет'}"
                f"\n<b>Дата регистрации:</b> {user.created_at.astimezone().strftime("%d.%m.%Y %H:%M:%S")}",
            attachments = [attachment.url for attachment in user.attachments]
        )
    )

@router.subscriber("users")
async def users(data: GetUsers) -> RabbitRequestResponse[GetUserResponse]:
    filters = {
        "all": True,
        "banned": User.is_banned,
        "verify": User.verify,
        "male": User.male,
        "female": not User.male,
        "inactive": not User.is_active
    }
    users = await UserRepository().get_all(data.offset, data.limit, filters[data.filter])
    total = await UserRepository().count(filters[data.filter])
    if not total:
        return RabbitRequestResponse(success = False, error = "Пользователи отсутсвуют")
    return RabbitRequestResponse(
        response = GetUsersResponse(
            text = 
                f"<b>Страница:</b> {math.ceil(data.offset / data.limit) + 1} / {math.ceil(total / data.limit)}\n\n"
                + '\n'.join([
                    f"{i}. {user.mention} (<code>{user.id}</code>){' 🚫' if user.is_banned else ''}{' ✅' if user.verify else ''}"
                    for i, user in enumerate(users, data.offset + 1)
                ]),
            count = len(users)
        )
    )