from sqlalchemy import ScalarResult
from sqlmodel import select, insert
from infrastructure.db import BaseRepository, Attachment, User


class AttachmentRepository(BaseRepository):

    async def get(self, id: str) -> Attachment | None:
        query = select(Attachment).where(Attachment.id == id)
        res = await self.session.exec(query)
        return res.first()
    
    async def insert(self, id: str, filetype: str, user: User) -> Attachment:
        atch = Attachment(
            id = id,
            filetype = filetype,
            user = user
        )
        self.session.add(atch)
        await self.session.flush()
        await self.session.refresh(user)
        return atch
    
    async def delete(self, attachment: Attachment) -> None:
        await self.session.delete(attachment)
        await self.session.flush()