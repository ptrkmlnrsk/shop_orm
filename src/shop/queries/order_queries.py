import sqlalchemy as sa

from sqlalchemy.sql import Select, func, or_
from src.shop.models.order import Order
from src.shop.models.order_item import OrderItem
from src.shop.models.employee import Employee

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
        Employee.end_date
        ).select_from(Order)
                .join(OrderItem, Order.order_id==OrderItem.order_id) # jak zrobić inner join?
                .join(Employee, Order.employee_id==Employee.employee_id))
                .group_by(Order.order_id, Employee.end_date)
                .subquery('orders_ids_and_employees'))


    return (
        sa.select(
            subquery.c.order_id)
        .filter(or_(subquery.c.items_in_order > 51,
                    subquery.c.end_date.isnot(None)
        ))
    )