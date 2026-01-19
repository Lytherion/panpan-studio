import json
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from fastapi import HTTPException
from app.models.product import Product, ProductSize
from app.schemas.product import ProductCreate, ProductUpdate, ProductList

async def get_products(db: AsyncSession, skip: int = 0, limit: int = 50):
    result = await db.execute(
        select(Product)
        .where(Product.is_active == True)
        .offset(skip)
        .limit(limit)
    )
    products = result.scalars().all()

    product_list = []
    for product in products:
        sizes = await db.execute(
            select(ProductSize).where(ProductSize.product_id == product.id)
        )
        sizes_list = sizes.scalars().all()

        if sizes_list:
            min_price = min(s.price for s in sizes_list)
            in_stock = any(s.stock > 0 for s in sizes_list)
        else:
            min_price = 0
            in_stock = False

        product_list.append(ProductList(
            id=product.id,
            title=product.title,
            images=product.images,
            min_price=min_price,
            is_active=product.is_active,
            in_stock=in_stock
        ))

    return product_list

async def get_product(db: AsyncSession, product_id: int):
    result = await db.execute(
        select(Product).where(Product.id == product_id)
    )
    product = result.scalar_one_or_none()

    if not product:
        raise HTTPException(status_code=404, detail="商品不存在")

    return product

async def create_product(db: AsyncSession, product_data: ProductCreate):
    product = Product(
        title=product_data.title,
        description=product_data.description,
        images=product_data.images,
        video_url=product_data.video_url
    )
    db.add(product)
    await db.flush()

    for size_data in product_data.sizes:
        size = ProductSize(
            product_id=product.id,
            size_name=size_data.size_name,
            price=size_data.price,
            stock=size_data.stock
        )
        db.add(size)

    await db.commit()
    await db.refresh(product)
    return product

async def update_product(db: AsyncSession, product_id: int, product_data: ProductUpdate):
    product = await get_product(db, product_id)

    product.title = product_data.title
    product.description = product_data.description
    product.images = product_data.images
    product.video_url = product_data.video_url

    if product_data.is_active is not None:
        product.is_active = product_data.is_active

    if product_data.sizes:
        # 删除旧尺码
        await db.execute(
            select(ProductSize).where(ProductSize.product_id == product_id)
        )

        # 添加新尺码
        for size_data in product_data.sizes:
            if size_data.id:
                result = await db.execute(
                    select(ProductSize).where(ProductSize.id == size_data.id)
                )
                size = result.scalar_one_or_none()
                if size:
                    size.size_name = size_data.size_name
                    size.price = size_data.price
                    size.stock = size_data.stock
            else:
                size = ProductSize(
                    product_id=product.id,
                    size_name=size_data.size_name,
                    price=size_data.price,
                    stock=size_data.stock
                )
                db.add(size)

    await db.commit()
    await db.refresh(product)
    return product

async def delete_product(db: AsyncSession, product_id: int):
    product = await get_product(db, product_id)
    await db.delete(product)
    await db.commit()
