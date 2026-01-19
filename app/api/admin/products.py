from fastapi import APIRouter, Depends, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.models.user import User
from app.utils.security import get_current_admin_user
from app.services import product as product_service
from app.schemas.product import ProductCreate, ProductUpdate, Product
from app.utils.upload import save_upload_file

router = APIRouter(prefix="/admin/products", tags=["管理员-商品管理"])

@router.post("/", response_model=Product, summary="创建商品")
async def create_product(
    product_data: ProductCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)
):
    return await product_service.create_product(db, product_data)

@router.put("/{product_id}", response_model=Product, summary="更新商品")
async def update_product(
    product_id: int,
    product_data: ProductUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)
):
    return await product_service.update_product(db, product_id, product_data)

@router.delete("/{product_id}", summary="删除商品")
async def delete_product(
    product_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)
):
    await product_service.delete_product(db, product_id)
    return {"message": "删除成功"}

@router.post("/upload", summary="上传商品图片/视频")
async def upload_file(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_admin_user)
):
    file_path = await save_upload_file(file, "products")
    return {"file_path": file_path}
