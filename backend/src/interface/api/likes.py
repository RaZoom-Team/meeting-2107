from fastapi import APIRouter, Body, Depends

from src.application.auth import get_user
from src.application.likes import LikeService
from src.application.user import UserService
from src.domain.user import FullUserDTO, FriendUserDTO, ReportUser
from src.infrastructure.db import User, CTX_SESSION

router = APIRouter(prefix="/user/likes", tags=["Likes"])


@router.post(
    "",
    responses={
        403: {"description": "Focus user not selected (3003)"}
    }
)
async def send_like(status: bool = Body(embed=True), user: User = Depends(get_user)) -> FullUserDTO:
    """
    Ответ на текущую анкету
    """
    await LikeService().answer_focus(user, status)
    await CTX_SESSION.get().commit()
    return user


@router.post(
    "/report",
    responses={
        403: {"description": "Focus user not selected (3003)"}
    }
)
async def report_user(report: ReportUser, user: User = Depends(get_user)) -> FullUserDTO:
    """
    Репорт текущей анкеты
    """
    await UserService().report_focus(user, report.reason)
    await CTX_SESSION.get().commit()
    return user


@router.get("")
async def get_likes(user: User = Depends(get_user)) -> list[FriendUserDTO]:
    """
    Получение всех взаимных лайков
    """
    return await LikeService().get_all_mutually(user)
