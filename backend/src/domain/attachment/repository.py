from sqlmodel import select, insert
from infrastructure.db import BaseRepository, Attachment


class AttachmentRepository(BaseRepository):

    async def get(self, id: str) -> Attachment | None:
        query = select(Attachment).where(Attachment.id == id)
        res = await self.session.exec(query)
        return res.first()
    
    async def insert(self, id: str, filetype: str, user_id: int) -> Attachment:
        query = insert(Attachment).values(
            id = id,
            filetype = filetype,
            user_id = user_id
        ).returning(Attachment)
        res = await self.session.exec(query)
        return res.scalar_one()