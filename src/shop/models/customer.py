from typing import TYPE_CHECKING

from src.shop.db.base import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, String

if TYPE_CHECKING:
    from src.shop.models.order import Order
    from src.shop.models.customer_address import CustomerAddress


class Customer(Base):
    __tablename__ = "customers"

    customer_id: Mapped[int] = mapped_column(primary_key=True, unique=True)
    first_name: Mapped[str]
    last_name: Mapped[str]
    phone_number: Mapped[str]
    email: Mapped[str] = mapped_column(String(30))

    address_id: Mapped[int] = mapped_column(ForeignKey("customer_addresses.id"), unique=True, nullable=False)
    customer_address: Mapped["CustomerAddress"] = relationship(back_populates="customer")
    orders: Mapped[list["Order"]] = relationship(back_populates="customer")
