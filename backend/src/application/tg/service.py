import aiohttp

from domain.telegram import SendMediaTelegramMessage, SendTelegramMessage
from config import TG_API_URL, TG_CHANNEL_ID
from infrastructure.db import User
from infrastructure.rabbit.router import broker


class TelegramService:

    async def _request(self, path: str, data: dict) -> aiohttp.ClientResponse:
        async with aiohttp.ClientSession() as session:
            return await session.post(TG_API_URL + path, json=data)

    async def check_subscribed(self, user_id: int) -> bool:
        res = await self._request("/getChatMember", {
            "chat_id": TG_CHANNEL_ID,
            "user_id": user_id
        })
        return res.ok and (await res.json())['result']['status'] not in ["left", "kicked"]

    async def send_message(self, text: str, *, chat_id: int) -> None:
        await broker.publish(
            SendTelegramMessage(chat_id = chat_id, text = text),
            "tg_msg"
        )

    async def send_to_chat(self, text: str) -> None:
        await self.send_message(text, chat_id = -1)

    async def send_media_to_chat(self, text: str, files: list[str]) -> None:
        await broker.publish(
            SendMediaTelegramMessage(chat_id = -1, text = text, files = files),
            "tg_media"
        )

    async def send_report(self, user: User, target: User, reason: str) -> None:
        pass