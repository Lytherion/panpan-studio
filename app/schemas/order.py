from pydantic import BaseModel
from datetime import datetime

class OrderItemCreate(BaseModel):
    product_id: int
    size_id: int
    quantity: int

class OrderItem(BaseModel):
    id: int
    product_title: str
    size_name: str
    price: float
    quantity: int
    subtotal: float

    class Config:
        from_attributes = True

class OrderCreate(BaseModel):
    recipient_name: str
    recipient_phone: str
    recipient_address: str
    items: list[OrderItemCreate]

class OrderUpdate(BaseModel):
    status: str | None = None
    reject_reason: str | None = None
    tracking_no: str | None = None

class Order(BaseModel):
    id: int
    order_no: str
    recipient_name: str
    recipient_phone: str
    recipient_address: str
    total_amount: float
    shipping_fee: float
    final_amount: float
    status: str
    payment_image: str | None = None
    reject_reason: str | None = None
    tracking_no: str | None = None
    created_at: datetime
    updated_at: datetime
    items: list[OrderItem]

    class Config:
        from_attributes = True

class OrderList(BaseModel):
    id: int
    order_no: str
    recipient_name: str
    final_amount: float
    status: str
    created_at: datetime

    class Config:
        from_attributes = True
