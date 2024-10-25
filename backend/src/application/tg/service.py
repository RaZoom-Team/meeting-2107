import asyncio
import aiohttp

from config import TG_API_URL, TG_ADMIN_CHAT


class TelegramService:

    async def _send_message(self, text: str, *, chat_id: int | None = None, user_id: int | None = None) -> None:
        peer_id = chat_id or user_id
        async with aiohttp.ClientSession() as session:
            await session.post(TG_API_URL + "/sendMessage", json={
                "chat_id": peer_id,
                "text": text,
                "parse_mode": "html"
            })

    async def send_message(self, text: str, *, chat_id: int | None = None, user_id: int | None = None) -> None:
        asyncio.ensure_future(self._send_message(text, chat_id=chat_id, user_id=user_id))

    async def send_to_chat(self, text: str) -> None:
        await self.send_message(text, chat_id = TG_ADMIN_CHAT)