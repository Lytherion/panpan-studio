from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.schemas.user import UserLogin, Token
from app.services import auth as auth_service

router = APIRouter(prefix="/admin/auth", tags=["管理员认证"])

@router.post("/login", response_model=Token, summary="管理员登录")
async def admin_login(
    login_data: UserLogin,
    db: AsyncSession = Depends(get_db)
):
    return await auth_service.authenticate_user(db, login_data)
