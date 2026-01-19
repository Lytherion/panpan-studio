from sqlalchemy import Column, Integer, String, Float, Text, DateTime, Enum, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from app.database import Base

class OrderStatus(enum.Enum):
    PENDING_PAYMENT = "pending_payment"      # 待付款
    PENDING_REVIEW = "pending_review"        # 待审核
    CONFIRMED = "confirmed"                   # 已确认
    REJECTED = "rejected"                     # 已拒绝
    SHIPPED = "shipped"                       # 已发货

class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    order_no = Column(String(50), unique=True, index=True, nullable=False)
    session_id = Column(String(100), index=True, nullable=False)

    # 收货信息
    recipient_name = Column(String(50), nullable=False)
    recipient_phone = Column(String(20), nullable=False)
    recipient_address = Column(String(500), nullable=False)

    # 金额
    total_amount = Column(Float, nullable=False)
    shipping_fee = Column(Float, default=0)
    final_amount = Column(Float, nullable=False)

    # 状态
    status = Column(Enum(OrderStatus), default=OrderStatus.PENDING_PAYMENT)
    payment_image = Column(String(500))  # 付款截图
    reject_reason = Column(Text)  # 拒绝原因
    tracking_no = Column(String(100))  # 物流单号

    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    items = relationship("OrderItem", back_populates="order", cascade="all, delete-orphan")

class OrderItem(Base):
    __tablename__ = "order_items"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    size_id = Column(Integer, ForeignKey("product_sizes.id"), nullable=False)
    product_title = Column(String(200), nullable=False)
    size_name = Column(String(50), nullable=False)
    price = Column(Float, nullable=False)
    quantity = Column(Integer, nullable=False)
    subtotal = Column(Float, nullable=False)

    order = relationship("Order", back_populates="items")
