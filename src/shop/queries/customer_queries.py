import sqlalchemy as sa

from sqlalchemy.sql import Select
from sqlalchemy import func

from src.shop.models.customer import Customer
from src.shop.models.customer_address import CustomerAddress
from src.shop.models.product import Product
from src.shop.models.order import Order
from src.shop.models.order_item import OrderItem


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



def calculate_min_max_customer_spent():

    subquery = (
        sa.select(
        Order.customer_id,
        func.sum(Product.current_price * OrderItem.quantity).label("total_spent")
    ).select_from(Order)
    .join(OrderItem, Order.order_id == OrderItem.order_id)
    .join(Product, OrderItem.product_id == Product.product_id)
        .group_by(Order.customer_id)
        .subquery("customers_total_spent")
    )
    return (
        sa.select(
            #func.max(subq.c.total_spent).label('max_spent'),
            #func.min(subq.c.total_spent).label('min_spent')
            (func.max(subquery.c.total_spent) - func.min(subquery.c.total_spent)).label('difference_in_spent')
        ).select_from(subquery)
    )

