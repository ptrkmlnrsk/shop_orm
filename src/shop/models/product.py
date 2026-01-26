from src.shop.db.base import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from src.shop.models.order_item import OrderItem
from src.shop.models.product_inventory import ProductInventory


class Product(Base):
    __tablename__ = "products"
    id: Mapped[int] = mapped_column(primary_key=True, index=True, unique=True)
    product_name: Mapped[str]
    brand: Mapped[str]
    category_id: Mapped[int] = mapped_column(ForeignKey("categories.id"), nullable=False)

    product_inventories: Mapped[list["ProductInventory"]] = relationship(
        back_populates="product")
    order_item_id: Mapped[list["OrderItem"]] = relationship(back_populates="product")
