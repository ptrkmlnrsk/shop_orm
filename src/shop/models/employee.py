import datetime

from src.shop.db.base import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.shop.models.order import Order


class Employee(Base):
    __tablename__ = "employees"

    id: Mapped[int] = mapped_column(primary_key=True, index=True, unique=True)
    first_name: Mapped[str]
    last_name: Mapped[str]
    phone_number: Mapped[str]
    email: Mapped[str]
    start_date: Mapped[datetime.datetime]
    end_date: Mapped[datetime.datetime | None]

    orders: Mapped[list["Order"]] = relationship(back_populates="employee")
