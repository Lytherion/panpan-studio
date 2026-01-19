from pydantic import BaseModel

class CartItemAdd(BaseModel):
    product_id: int
    size_id: int
    quantity: int = 1

class CartItemUpdate(BaseModel):
    quantity: int

class CartItem(BaseModel):
    id: int
    product_id: int
    size_id: int
    product_title: str
    size_name: str
    price: float
    quantity: int
    subtotal: float
    image: str | None = None

    class Config:
        from_attributes = True
