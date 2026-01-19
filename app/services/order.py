import uuid
import json
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from fastapi import HTTPException
from app.models.order import Order, OrderItem, OrderStatus
from app.models.product import Product, ProductSize
from app.schemas.order import OrderCreate, OrderUpdate
from app.config import settings

async def create_order(db: AsyncSession, session_id: str, order_data: OrderCreate):
    # 验证商品和库存
    total_amount = 0
    order_items = []

    for item_data in order_data.items:
        product_result = await db.execute(
            select(Product).where(Product.id == item_data.product_id)
        )
        product = product_result.scalar_one_or_none()

        size_result = await db.execute(
            select(ProductSize).where(ProductSize.id == item_data.size_id)
        )
        size = size_result.scalar_one_or_none()

        if not product or not size:
            raise HTTPException(status_code=404, detail="商品不存在")

        if size.stock < item_data.quantity:
            raise HTTPException(status_code=400, detail=f"{product.title} 库存不足")

        subtotal = size.price * item_data.quantity
        total_amount += subtotal

        order_items.append({
            "product": product,
            "size": size,
            "quantity": item_data.quantity,
            "subtotal": subtotal
        })

    # 创建订单
    order_no = f"ORD{datetime.now().strftime('%Y%m%d%H%M%S')}{uuid.uuid4().hex[:6].upper()}"
    final_amount = total_amount + settings.SHIPPING_FEE

    order = Order(
        order_no=order_no,
        session_id=session_id,
        recipient_name=order_data.recipient_name,
        recipient_phone=order_data.recipient_phone,
        recipient_address=order_data.recipient_address,
        total_amount=total_amount,
        shipping_fee=settings.SHIPPING_FEE,
        final_amount=final_amount,
        status=OrderStatus.PENDING_PAYMENT
    )
    db.add(order)
    await db.flush()

    # 创建订单项并锁定库存
    for item in order_items:
        order_item = OrderItem(
            order_id=order.id,
            product_id=item["product"].id,
            size_id=item["size"].id,
            product_title=item["product"].title,
            size_name=item["size"].size_name,
            price=item["size"].price,
            quantity=item["quantity"],
            subtotal=item["subtotal"]
        )
        db.add(order_item)

        # 锁定库存
        item["size"].stock -= item["quantity"]

    await db.commit()
    await db.refresh(order)
    return order

async def get_order(db: AsyncSession, order_id: int, session_id: str = None):
    query = select(Order).where(Order.id == order_id)
    if session_id:
        query = query.where(Order.session_id == session_id)

    result = await db.execute(query)
    order = result.scalar_one_or_none()

    if not order:
        raise HTTPException(status_code=404, detail="订单不存在")

    return order

async def get_orders(db: AsyncSession, session_id: str = None, skip: int = 0, limit: int = 50):
    query = select(Order)
    if session_id:
        query = query.where(Order.session_id == session_id)

    query = query.offset(skip).limit(limit).order_by(Order.created_at.desc())
    result = await db.execute(query)
    return result.scalars().all()

async def upload_payment_proof(db: AsyncSession, order_id: int, session_id: str, file_path: str):
    order = await get_order(db, order_id, session_id)

    if order.status != OrderStatus.PENDING_PAYMENT:
        raise HTTPException(status_code=400, detail="订单状态不允许上传付款凭证")

    order.payment_image = file_path
    order.status = OrderStatus.PENDING_REVIEW
    await db.commit()
    return order

async def review_order(db: AsyncSession, order_id: int, approved: bool, reject_reason: str = None):
    order = await get_order(db, order_id)

    if order.status != OrderStatus.PENDING_REVIEW:
        raise HTTPException(status_code=400, detail="订单状态不允许审核")

    if approved:
        order.status = OrderStatus.CONFIRMED
    else:
        order.status = OrderStatus.REJECTED
        order.reject_reason = reject_reason

        # 回滚库存
        items_result = await db.execute(
            select(OrderItem).where(OrderItem.order_id == order_id)
        )
        items = items_result.scalars().all()

        for item in items:
            size_result = await db.execute(
                select(ProductSize).where(ProductSize.id == item.size_id)
            )
            size = size_result.scalar_one_or_none()
            if size:
                size.stock += item.quantity

    await db.commit()
    await db.refresh(order)
    return order

async def update_order_status(db: AsyncSession, order_id: int, order_data: OrderUpdate):
    order = await get_order(db, order_id)

    if order_data.status:
        order.status = OrderStatus(order_data.status)

    if order_data.tracking_no:
        order.tracking_no = order_data.tracking_no
        order.status = OrderStatus.SHIPPED

    await db.commit()
    await db.refresh(order)
    return order
