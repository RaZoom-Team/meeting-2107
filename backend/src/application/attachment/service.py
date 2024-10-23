import io
import os
import uuid
import aiofiles
from PIL import Image

from domain.attachment import AttachmentRepository
from infrastructure.db import Attachment
from infrastructure.exc import InvalidImageException, NotFound


class AttachmentService:

    def __init__(self) -> None:
        self.repo = AttachmentRepository()

    async def save_file(self, file: bytes, id: str, filetype: str) -> None:
        try:
            img_data = io.BytesIO()
            with Image.open(io.BytesIO(file)) as img:
                img.save(img_data, filetype, optimize=True, quality=95)
            if not os.path.exists("data"):
                os.mkdir("data")
            async with aiofiles.open(f"data/{id}.{filetype}", "wb") as f:
                img_data.seek(0)
                await f.write(img_data.read())
        except OSError:
            raise InvalidImageException

    async def upload(self, file: bytes, user_id: int) -> Attachment:
        atch = await self.repo.insert(id = str(uuid.uuid4()), filetype = "jpeg", user_id = user_id)
        await self.save_file(file, atch.id, atch.filetype)
        return atch
    
    async def download_file(self, id: str) -> tuple[bytes, str]:
        atch = await self.repo.get(id)
        if not atch: raise NotFound()

        async with aiofiles.open(f"data/{atch.id}.{atch.filetype}", "rb") as f:
            return await f.read(), atch.filetype