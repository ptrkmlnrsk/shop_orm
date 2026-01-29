from typing import TYPE_CHECKING

from src.shop.db.base import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
if TYPE_CHECKING:
    from src.shop.models.customer import Customer

class CustomerAddress(Base):
    __tablename__ = "customer_addresses"

    address_id: Mapped[int] = mapped_column(primary_key=True, unique=True)
    country: Mapped[str]
    city: Mapped[str]
    postal_code: Mapped[str]

    customer: Mapped["Customer"] = relationship(back_populates="customer_address", uselist=False)
