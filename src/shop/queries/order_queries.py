import sqlalchemy as sa

from sqlalchemy.sql import Select, func, or_, text
from src.shop.models.order import Order
from src.shop.models.order_item import OrderItem
from src.shop.models.employee import Employee
from src.shop.models.customer import Customer
from src.shop.models.product import Product

def count_duplicated_orders():
    return (
        sa.select(
            Order.customer_id,
        ).group_by(Order.customer_id).having(
            sa.func.count() > 1)
    )

def count_orders_with_at_least_51_items_by_employees():

    subquery = ((sa.select(
        Order.order_id,
        func.sum(OrderItem.quantity).label('items_in_order'),
        Order.order_date,
        Employee.end_date
        ).select_from(Order)
                .join(OrderItem, Order.order_id==OrderItem.order_id) # jak zrobić inner join?
                .join(Employee, Order.employee_id==Employee.employee_id))
            .group_by(Order.order_id, Order.order_date, Employee.end_date)
                .subquery('orders_ids_and_employees'))

    # subquery do przeliczania tego co potrzebuje
    # ewentualnie 2 subquery i potem UNION

    return (
        sa.select(
            subquery.c.order_id)
        .filter(or_(subquery.c.items_in_order > 50,
                    subquery.c.end_date.is_(None)
        ))
    )


def find_customers_that_made_orders_in_2017():

    return (
        sa.select(
            Order.customer_id,
            Customer.first_name,
            Customer.last_name
        ).select_from(Order)
        .join(Customer, Order.customer_id==Customer.customer_id)
        #.where(sa.extract("year", Order.order_date) == 2017)
        .where(Order.order_date >= sa.literal('2017-01-01'),
               Order.order_date < sa.literal('2018-01-01'))
    )


def count_total_sales_per_month():

    return (
        sa.select(
            func.sum(Product.current_price * OrderItem.quantity).label('total_sales'),
            sa.extract('month', Order.order_date).label('month_extract')
        ).select_from(Order)
            .join(OrderItem, Order.order_id==OrderItem.order_id)
            .join(Product, OrderItem.product_id==Product.product_id)
            .group_by(sa.extract('month', Order.order_date).label('month_extract'))
            .order_by('month_extract')
        )


def avg_days_to_complete_order():

    subquery = sa.select(
        Order.store_id,
        func.datediff(text('day'), Order.order_date, Order.shipped_date).label('days_to_complete_order')
    ).select_from(Order).subquery('days_for_order')

    return (
        sa.select(subquery.c.store_id,
                  func.avg(subquery.c.days_to_complete_order))
        .group_by(subquery.c.store_id)
        .order_by(subquery.c.store_id.asc())
    )