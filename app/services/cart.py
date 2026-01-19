import json
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from fastapi import HTTPException
from app.models.cart import Cart
from app.models.product import Product, ProductSize
from app.schemas.cart import CartItemAdd, CartItemUpdate, CartItem

async def get_cart_items(db: AsyncSession, session_id: str):
    result = await db.execute(
        select(Cart).where(Cart.session_id == session_id)
    )
    cart_items = result.scalars().all()

    items = []
    for cart_item in cart_items:
        product_result = await db.execute(
            select(Product).where(Product.id == cart_item.product_id)
        )
        product = product_result.scalar_one_or_none()

        size_result = await db.execute(
            select(ProductSize).where(ProductSize.id == cart_item.size_id)
        )
        size = size_result.scalar_one_or_none()

        if product and size:
            image = json.loads(product.images)[0] if product.images else None
            items.append(CartItem(
                id=cart_item.id,
                product_id=cart_item.product_id,
                size_id=cart_item.size_id,
                product_title=product.title,
                size_name=size.size_name,
                price=size.price,
                quantity=cart_item.quantity,
                subtotal=size.price * cart_item.quantity,
                image=image
            ))

    return items

async def add_cart_item(db: AsyncSession, session_id: str, item_data: CartItemAdd):
    # 检查商品和尺码
    size_result = await db.execute(
        select(ProductSize).where(ProductSize.id == item_data.size_id)
    )
    size = size_result.scalar_one_or_none()

    if not size or size.stock < item_data.quantity:
        raise HTTPException(status_code=400, detail="库存不足")

    # 检查购物车是否已有该商品
    result = await db.execute(
        select(Cart).where(
            Cart.session_id == session_id,
            Cart.product_id == item_data.product_id,
            Cart.size_id == item_data.size_id
        )
    )
    cart_item = result.scalar_one_or_none()

    if cart_item:
        cart_item.quantity += item_data.quantity
    else:
        cart_item = Cart(
            session_id=session_id,
            product_id=item_data.product_id,
            size_id=item_data.size_id,
            quantity=item_data.quantity
        )
        db.add(cart_item)

    await db.commit()
    return {"message": "添加成功"}

async def update_cart_item(db: AsyncSession, session_id: str, cart_id: int, item_data: CartItemUpdate):
    result = await db.execute(
        select(Cart).where(Cart.id == cart_id, Cart.session_id == session_id)
    )
    cart_item = result.scalar_one_or_none()

    if not cart_item:
        raise HTTPException(status_code=404, detail="购物车项不存在")

    # 检查库存
    size_result = await db.execute(
        select(ProductSize).where(ProductSize.id == cart_item.size_id)
    )
    size = size_result.scalar_one_or_none()

    if not size or size.stock < item_data.quantity:
        raise HTTPException(status_code=400, detail="库存不足")

    cart_item.quantity = item_data.quantity
    await db.commit()
    return {"message": "更新成功"}

async def delete_cart_item(db: AsyncSession, session_id: str, cart_id: int):
    result = await db.execute(
        delete(Cart).where(Cart.id == cart_id, Cart.session_id == session_id)
    )

    if result.rowcount == 0:
        raise HTTPException(status_code=404, detail="购物车项不存在")

    await db.commit()
    return {"message": "删除成功"}

async def clear_cart(db: AsyncSession, session_id: str):
    await db.execute(delete(Cart).where(Cart.session_id == session_id))
    await db.commit()
    return {"message": "购物车已清空"}
