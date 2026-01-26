from src.shop.db.base import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.shop.models.customer import Customer

class CustomerAddress(Base):
    __tablename__ = "customer_addresses"

    id: Mapped[int] = mapped_column(primary_key=True, unique=True)
    country: Mapped[str]
    city: Mapped[str]
    postal_code: Mapped[str]

    customers: Mapped[list["Customer"]] = relationship(back_populates="customer_address")
