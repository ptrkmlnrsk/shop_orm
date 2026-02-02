import sqlalchemy as sa

from sqlalchemy.sql import Select
from sqlalchemy import func

from src.shop.models.employee import Employee
from src.shop.models.customer_address import CustomerAddress
from src.shop.models.store import Store



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