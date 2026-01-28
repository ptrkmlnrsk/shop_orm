import sqlalchemy as sa
from src.shop.models.customer import Customer

def customer_by_name(first_name: str):
    return sa.select(Customer).where(Customer.first_name.ilike(f"%{first_name}"))