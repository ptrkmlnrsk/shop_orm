import sqlalchemy as sa

from sqlalchemy.sql import Select
from sqlalchemy import func, text
from src.shop.models.employee import Employee
from src.shop.models.customer_address import CustomerAddress
from src.shop.models.store import Store
from src.shop.models.order import Order
from src.shop.models.order_item import OrderItem


def check_if_employee_is_employed_and_how_long() -> Select:
    employment_status_case = sa.case(
        (Employee.end_date.is_(None), 'employed'),
        else_='not employed'
    ).label('employment_status')

    return (
        sa.select(
            Employee.employee_id,
            Employee.first_name,
            Employee.last_name,
            Employee.start_date,
            Employee.end_date,
            func.datediff(sa.literal_column("day"), Employee.start_date, sa.func.getdate()).label("days_employed"),
            employment_status_case
        )
    )



def find_customer_cities_without_stores() -> Select:
    return (
        sa.select(
            CustomerAddress.address_id,
            CustomerAddress.country,
            CustomerAddress.city,
            CustomerAddress.street,
            CustomerAddress.postal_code
        )
        .select_from(CustomerAddress)
        .where(CustomerAddress.city
               .not_in(
                    sa.select(Store.city).select_from(Store)
                )
            )
        ).distinct()


def show_all_employees_names() -> Select:
    return (
        sa.select(
            func.concat(Employee.first_name, ' ', Employee.last_name).label("full_name")
        )
    )


def get_employee_and_sales_sum_in_2022_2023() -> Select:


    year_2022_sum = func.sum(
                sa.case(
                    (sa.extract("year", Order.order_date)==2022, OrderItem.quantity),
            else_=0)).label('sales_sum_2022')

    year_2023_sum = func.sum(
                sa.case(
                    (sa.extract("year", Order.order_date)==2023, OrderItem.quantity),
            else_=0)).label('sales_sum_2023')


    query = (
        sa.select(
            Employee.employee_id,
            Employee.first_name,
            year_2022_sum,
            year_2023_sum
        ).select_from(Employee)
        .outerjoin(Order, Employee.employee_id==Order.employee_id)
        .outerjoin(OrderItem, Order.order_id==OrderItem.order_id)
        .group_by(Employee.employee_id, Employee.first_name)
    )

    return query