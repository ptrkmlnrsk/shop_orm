from src.shop.db.base import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.shop.models.order import Order
from src.shop.models.product_inventory import ProductInventory

class Store(Base):
    __tablename__ = "stores"

    id: Mapped[int] = mapped_column(primary_key=True, index=True, unique=True)
    store_name: Mapped[str]
    country: Mapped[str]
    city: Mapped[str]
    street: Mapped[str]
    postal_code: Mapped[str]
    store_size: Mapped[int]

    orders: Mapped[list["Order"]] = relationship(back_populates="store") # jesli po jednej stronie mam liste zamowien to po drugiej mam jeden sklep
    product_inventories: Mapped[list["ProductInventory"]] = relationship(back_populates="store")
