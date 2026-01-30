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

    address_id: Mapped[int] = mapped_column(ForeignKey("customer_addresses.address_id"), unique=True, nullable=False)
    customer_address: Mapped["CustomerAddress"] = relationship(back_populates="customer")
    orders: Mapped[list["Order"]] = relationship(back_populates="customer")

    def __repr__(self) -> str:
        return(
            f"Customer("
            f"customer_id={self.customer_id}, "
            f"first_name={self.first_name}, "
            f"last_name={self.last_name}, "
            f"phone_number={self.phone_number}, "
            f"email={self.email}, "
        )
