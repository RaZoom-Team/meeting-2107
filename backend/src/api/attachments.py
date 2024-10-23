from fastapi import APIRouter
from fastapi.responses import Response

from application.attachment.service import AttachmentService


router = APIRouter(prefix="/attachments", tags=["Attachments"])


@router.get(
    "/{attachment_id}",
    responses = {
        404: {"description": "Not found"}
    }
)
async def download_attachment(attachment_id: str) -> bytes:
    """
    Получение файла вложения
    """
    file, filetype = await AttachmentService().download_file(attachment_id)
    return Response(
        content = file,
        media_type = "image/" + filetype
    )