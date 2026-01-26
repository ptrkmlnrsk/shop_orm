from sqlalchemy.orm import sessionmaker
from src.shop.db.engine import engine

Session = sessionmaker(bind=engine)