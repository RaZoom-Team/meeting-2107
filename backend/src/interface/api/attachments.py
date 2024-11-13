from fastapi import APIRouter
from fastapi.responses import Response

from src.application.attachment import AttachmentService


router = APIRouter(prefix="/attachments", tags=["Attachments"])


@router.get(
    "/{attachment_id}",
    responses = {
        404: {"description": "Not found (1000)"},
        400: {"description": "undefined in endpoint"},
        401: {"description": "undefined in endpoint"}
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
