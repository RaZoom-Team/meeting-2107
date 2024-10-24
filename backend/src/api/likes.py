from fastapi import APIRouter, Body, Depends

from application.auth import get_user
from application.likes import LikeService
from domain.user import UserDTO, FullUserDTO
from infrastructure.db import User, CTX_SESSION

router = APIRouter(prefix="/user/likes", tags=["Likes"])

@router.post(
    "",
    responses={
        403: {"description": "Focus user not selected"}
    }
)
async def send_like(status: bool = Body(embed=True), user: User = Depends(get_user)) -> FullUserDTO:
    """
    Ответ на текущую анкету
    """
    await LikeService().answer_focus(user, status)
    await CTX_SESSION.get().commit()
    return user

@router.get("")
async def get_likes(user: User = Depends(get_user)) -> list[UserDTO]:
    """
    Получение всех взаимных лайков
    """
    return await LikeService().get_all_mutually(user)