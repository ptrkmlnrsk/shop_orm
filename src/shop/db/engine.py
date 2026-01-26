import sqlalchemy as sa
from src.shop.config import DATABASE_URL

engine = sa.create_engine(
    DATABASE_URL,
    echo=True)