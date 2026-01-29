from typing import TYPE_CHECKING

from src.shop.db.base import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.shop.models.product_inventory import ProductInventory

if TYPE_CHECKING:
    from src.shop.models.order import Order


class Store(Base):
    __tablename__ = "stores"

    store_id: Mapped[int] = mapped_column(primary_key=True, index=True, unique=True)
    store_name: Mapped[str]
    country: Mapped[str]
    city: Mapped[str]
    street: Mapped[str]
    postal_code: Mapped[str]
    store_size: Mapped[int]

    orders: Mapped[list["Order"]] = relationship(back_populates="store")
    product_inventories: Mapped[list["ProductInventory"]] = relationship(back_populates="store")
