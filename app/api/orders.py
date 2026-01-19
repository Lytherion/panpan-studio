from fastapi import APIRouter, Depends, Header, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.services import order as order_service
from app.schemas.order import OrderCreate, Order
from app.utils.upload import save_upload_file

router = APIRouter(prefix="/orders", tags=["订单"])

def get_session_id(x_session_id: str = Header(...)) -> str:
    return x_session_id

@router.post("/", response_model=Order, summary="创建订单")
async def create_order(
    order_data: OrderCreate,
    session_id: str = Depends(get_session_id),
    db: AsyncSession = Depends(get_db)
):
    return await order_service.create_order(db, session_id, order_data)

@router.get("/", summary="获取订单列表")
async def get_orders(
    session_id: str = Depends(get_session_id),
    db: AsyncSession = Depends(get_db)
):
    return await order_service.get_orders(db, session_id)

@router.get("/{order_id}", response_model=Order, summary="获取订单详情")
async def get_order(
    order_id: int,
    session_id: str = Depends(get_session_id),
    db: AsyncSession = Depends(get_db)
):
    return await order_service.get_order(db, order_id, session_id)

@router.post("/{order_id}/payment", summary="上传付款凭证")
async def upload_payment(
    order_id: int,
    file: UploadFile = File(...),
    session_id: str = Depends(get_session_id),
    db: AsyncSession = Depends(get_db)
):
    file_path = await save_upload_file(file, "payment")
    return await order_service.upload_payment_proof(db, order_id, session_id, file_path)
