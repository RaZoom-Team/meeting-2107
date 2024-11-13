from fastapi import APIRouter

from src.infrastructure.db.session import ping_db


router = APIRouter(prefix="/system", include_in_schema=False)

@router.get("/ping")
async def ping() -> bool:
    await ping_db()
    return True