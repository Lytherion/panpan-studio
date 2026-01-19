from fastapi import APIRouter, Depends, Header
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.services import cart as cart_service
from app.schemas.cart import CartItemAdd, CartItemUpdate

router = APIRouter(prefix="/cart", tags=["购物车"])

def get_session_id(x_session_id: str = Header(...)) -> str:
    return x_session_id

@router.get("/", summary="获取购物车")
async def get_cart(
    session_id: str = Depends(get_session_id),
    db: AsyncSession = Depends(get_db)
):
    return await cart_service.get_cart_items(db, session_id)

@router.post("/", summary="添加到购物车")
async def add_to_cart(
    item: CartItemAdd,
    session_id: str = Depends(get_session_id),
    db: AsyncSession = Depends(get_db)
):
    return await cart_service.add_cart_item(db, session_id, item)

@router.put("/{cart_id}", summary="更新购物车项")
async def update_cart(
    cart_id: int,
    item: CartItemUpdate,
    session_id: str = Depends(get_session_id),
    db: AsyncSession = Depends(get_db)
):
    return await cart_service.update_cart_item(db, session_id, cart_id, item)

@router.delete("/{cart_id}", summary="删除购物车项")
async def delete_cart_item(
    cart_id: int,
    session_id: str = Depends(get_session_id),
    db: AsyncSession = Depends(get_db)
):
    return await cart_service.delete_cart_item(db, session_id, cart_id)

@router.delete("/", summary="清空购物车")
async def clear_cart(
    session_id: str = Depends(get_session_id),
    db: AsyncSession = Depends(get_db)
):
    return await cart_service.clear_cart(db, session_id)
