import asyncio
import aiohttp

from config import TG_API_URL, TG_ADMIN_CHAT, TG_CHANNEL_ID


class TelegramService:

    async def _request(self, path: str, data: dict) -> aiohttp.ClientResponse:
        async with aiohttp.ClientSession() as session:
            return await session.post(TG_API_URL + path, json=data)

    async def _send_message(self, text: str, *, chat_id: int | None = None, user_id: int | None = None) -> None:
        peer_id = chat_id or user_id
        await self._request("/sendMessage", {
            "chat_id": peer_id,
            "text": text,
            "parse_mode": "html"
        })

    async def check_subscribed(self, user_id: int) -> bool:
        res = await self._request("/getChatMember", {
            "chat_id": TG_CHANNEL_ID,
            "user_id": user_id
        })
        return res.ok and (await res.json())['result']['status'] not in ["left", "kicked"]

    async def send_message(self, text: str, *, chat_id: int | None = None, user_id: int | None = None) -> None:
        asyncio.ensure_future(self._send_message(text, chat_id=chat_id, user_id=user_id))

    async def send_to_chat(self, text: str) -> None:
        await self.send_message(text, chat_id = TG_ADMIN_CHAT)