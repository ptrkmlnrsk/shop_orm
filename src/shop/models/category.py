from src.shop.db.base import Base
from sqlalchemy.orm import Mapped, mapped_column

class Category(Base):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(primary_key=True,
                                    unique=True)
    category_name: Mapped[str]
