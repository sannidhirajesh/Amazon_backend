from datetime import datetime
from enum import Enum
from sqlalchemy import String,Text,Integer,Numeric,ForeignKey,DateTime,Enum as SAEnum
from sqlalchemy.orm import Mapped,mapped_column,relationship
from app.database.database import Base
class UserRole(str,Enum): CUSTOMER="CUSTOMER"; SELLER="SELLER"; ADMIN="ADMIN"
class OrderStatus(str,Enum): PENDING="PENDING"; CONFIRMED="CONFIRMED"; CANCELLED="CANCELLED"
class PaymentStatus(str,Enum): PENDING="PENDING"; SUCCESS="SUCCESS"; FAILED="FAILED"; REFUNDED="REFUNDED"
class User(Base):
    __tablename__="users"
    id:Mapped[int]=mapped_column(primary_key=True)
    name:Mapped[str]=mapped_column(String(120)); email:Mapped[str]=mapped_column(String(255),unique=True,index=True)
    password_hash:Mapped[str]=mapped_column(String(255)); phone:Mapped[str|None]=mapped_column(String(30))
    role:Mapped[UserRole]=mapped_column(SAEnum(UserRole,name="userrole",create_type=False),default=UserRole.CUSTOMER)
class Category(Base):
    __tablename__="categories"
    id:Mapped[int]=mapped_column(primary_key=True); name:Mapped[str]=mapped_column(String(120),unique=True)
class Product(Base):
    __tablename__="products"
    id:Mapped[int]=mapped_column(primary_key=True); seller_id:Mapped[int]=mapped_column(ForeignKey("users.id"))
    category_id:Mapped[int|None]=mapped_column(ForeignKey("categories.id"),nullable=True)
    name:Mapped[str]=mapped_column(String(200)); description:Mapped[str|None]=mapped_column(Text)
    price:Mapped[float]=mapped_column(Numeric(12,2)); brand:Mapped[str|None]=mapped_column(String(120))
    stock:Mapped[int]=mapped_column(Integer,default=0); sku:Mapped[str]=mapped_column(String(80),unique=True)
    image_url:Mapped[str|None]=mapped_column(String(500)); created_at:Mapped[datetime]=mapped_column(DateTime,default=datetime.utcnow)
class Cart(Base):
    __tablename__="carts"
    id:Mapped[int]=mapped_column(primary_key=True); user_id:Mapped[int]=mapped_column(ForeignKey("users.id"),unique=True)
    items=relationship("CartItem",cascade="all, delete-orphan")
class CartItem(Base):
    __tablename__="cart_items"
    id:Mapped[int]=mapped_column(primary_key=True); cart_id:Mapped[int]=mapped_column(ForeignKey("carts.id"))
    product_id:Mapped[int]=mapped_column(ForeignKey("products.id")); quantity:Mapped[int]=mapped_column(Integer)
    product=relationship("Product")
class Order(Base):
    __tablename__="orders"
    id:Mapped[int]=mapped_column(primary_key=True); user_id:Mapped[int]=mapped_column(ForeignKey("users.id"))
    status:Mapped[OrderStatus]=mapped_column(SAEnum(OrderStatus,name="orderstatus",create_type=False))
    total:Mapped[float]=mapped_column(Numeric(12,2)); shipping_address:Mapped[str|None]=mapped_column(Text)
    created_at:Mapped[datetime]=mapped_column(DateTime,default=datetime.utcnow)
    items=relationship("OrderItem",cascade="all, delete-orphan")
class OrderItem(Base):
    __tablename__="order_items"
    id:Mapped[int]=mapped_column(primary_key=True); order_id:Mapped[int]=mapped_column(ForeignKey("orders.id"))
    product_id:Mapped[int]=mapped_column(ForeignKey("products.id")); quantity:Mapped[int]=mapped_column(Integer)
    unit_price:Mapped[float]=mapped_column(Numeric(12,2))
class Payment(Base):
    __tablename__="payments"
    id:Mapped[int]=mapped_column(primary_key=True); order_id:Mapped[int]=mapped_column(ForeignKey("orders.id"),unique=True)
    method:Mapped[str]=mapped_column(String(40)); status:Mapped[PaymentStatus]=mapped_column(SAEnum(PaymentStatus,name="paymentstatus",create_type=False))
