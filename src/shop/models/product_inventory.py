from typing import TYPE_CHECKING

from src.shop.db.base import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey

if TYPE_CHECKING:
    from src.shop.models.product import Product
    from src.shop.models.store import Store

class ProductInventory(Base):
    __tablename__ = "product_inventories"

    id: Mapped[int] = mapped_column(primary_key=True, index=True, unique=True)
    quantity: Mapped[int]
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"))
    store_id: Mapped[int] = mapped_column(ForeignKey("stores.id"))

    product: Mapped["Product"] = relationship(back_populates="product_inventories")
    store: Mapped["Store"] = relationship(back_populates="product_inventories")

