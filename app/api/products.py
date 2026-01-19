from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.services import product as product_service
from app.schemas.product import Product

router = APIRouter(prefix="/products", tags=["商品"])

@router.get("/", summary="获取商品列表")
async def get_products(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    db: AsyncSession = Depends(get_db)
):
    return await product_service.get_products(db, skip, limit)

@router.get("/{product_id}", response_model=Product, summary="获取商品详情")
async def get_product(
    product_id: int,
    db: AsyncSession = Depends(get_db)
):
    return await product_service.get_product(db, product_id)
