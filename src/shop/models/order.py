import datetime

from typing import TYPE_CHECKING

from src.shop.db.base import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey

if TYPE_CHECKING:
    from src.shop.models.employee import Employee
    from src.shop.models.order_item import OrderItem
    from src.shop.models.store import Store
    from src.shop.models.customer import Customer


class Order(Base):
    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(primary_key=True, index=True, unique=True)
    order_status: Mapped[int]
    order_date: Mapped[datetime.datetime]
    shipped_date: Mapped[datetime.datetime]

    store_id: Mapped[int] = mapped_column(ForeignKey("stores.id"), nullable=False)
    employee_id: Mapped[int] = mapped_column(ForeignKey("employees.id"), nullable=False)
    customer_id: Mapped[int] = mapped_column(ForeignKey("customers.id"), nullable=False)

    store: Mapped["Store"] = relationship(back_populates="orders")
    employee: Mapped["Employee"] = relationship(back_populates="orders")
    customer: Mapped["Customer"] = relationship(back_populates="orders")
    order_item: Mapped[list["OrderItem"]] = relationship(back_populates="order")
