from typing import TYPE_CHECKING
from src.shop.db.base import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey

if TYPE_CHECKING:
    from src.shop.models.product import Product
    from src.shop.models.order import Order

class OrderItem(Base):
    __tablename__ = "order_items"

    order_item_id: Mapped[int] = mapped_column(primary_key=True, unique=True)
    quantity: Mapped[int]
    order_id: Mapped[int] = mapped_column(ForeignKey("orders.order_id"), nullable=False)
    discount_id: Mapped[int] = mapped_column(ForeignKey("product_discounts.discount_id"), nullable=False)
    product_id: Mapped[int] = mapped_column(ForeignKey("products.product_id"), nullable=False)

    order: Mapped[list["Order"]] = relationship(back_populates="order_item")
    product: Mapped["Product"] = relationship(back_populates="order_item_id")
