from pydantic import BaseModel
from datetime import datetime

class ProductSizeBase(BaseModel):
    size_name: str
    price: float
    stock: int

class ProductSizeCreate(ProductSizeBase):
    pass

class ProductSizeUpdate(ProductSizeBase):
    id: int | None = None

class ProductSize(ProductSizeBase):
    id: int
    product_id: int

    class Config:
        from_attributes = True

class ProductBase(BaseModel):
    title: str
    description: str | None = None
    images: str | None = None
    video_url: str | None = None

class ProductCreate(ProductBase):
    sizes: list[ProductSizeCreate]

class ProductUpdate(ProductBase):
    is_active: bool | None = None
    sizes: list[ProductSizeUpdate] | None = None

class Product(ProductBase):
    id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime
    sizes: list[ProductSize]

    class Config:
        from_attributes = True

class ProductList(BaseModel):
    id: int
    title: str
    images: str | None = None
    min_price: float
    is_active: bool
    in_stock: bool

    class Config:
        from_attributes = True
