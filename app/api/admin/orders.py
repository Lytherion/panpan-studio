from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.models.user import User
from app.utils.security import get_current_admin_user
from app.services import order as order_service
from app.schemas.order import Order, OrderUpdate

router = APIRouter(prefix="/admin/orders", tags=["管理员-订单管理"])

@router.get("/", summary="获取所有订单")
async def get_all_orders(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)
):
    return await order_service.get_orders(db, None, skip, limit)

@router.get("/{order_id}", response_model=Order, summary="获取订单详情")
async def get_order(
    order_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)
):
    return await order_service.get_order(db, order_id)

@router.post("/{order_id}/review", response_model=Order, summary="审核订单")
async def review_order(
    order_id: int,
    approved: bool = Query(...),
    reject_reason: str = Query(None),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)
):
    return await order_service.review_order(db, order_id, approved, reject_reason)

@router.put("/{order_id}", response_model=Order, summary="更新订单状态")
async def update_order(
    order_id: int,
    order_data: OrderUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)
):
    return await order_service.update_order_status(db, order_id, order_data)
