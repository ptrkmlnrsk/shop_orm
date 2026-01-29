from src.shop.db.base import Base
from sqlalchemy.orm import Mapped, mapped_column

class ProductDiscount(Base):
    __tablename__ = "product_discounts"

    discount_id: Mapped[int] = mapped_column(primary_key=True, unique=True)
    discount: Mapped[float]
    active: Mapped[int]

