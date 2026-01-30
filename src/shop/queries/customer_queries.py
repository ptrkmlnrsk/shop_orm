import sqlalchemy as sa
from src.shop.models.customer import Customer
from src.shop.models.customer_address import CustomerAddress
from sqlalchemy.sql import Select

def customer_by_name(first_name: str) -> Select:
    return sa.select(Customer).where(Customer.first_name.ilike(f"{first_name}"))

def customers_and_their_addresses() -> Select:
    return (
        sa.select(
            Customer.customer_id,
            Customer.first_name,
            Customer.last_name,
            CustomerAddress.country,
            CustomerAddress.city
        )
        .select_from(Customer)
        .join(Customer.customer_address)
    )