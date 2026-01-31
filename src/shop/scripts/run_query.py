from typing import TYPE_CHECKING
from src.shop.db.session import Session
from src.shop.models import Customer
from src.shop.scripts.file_handler import FileHandler

from src.shop.queries.customer_queries import (customer_by_name,
                                               customers_and_their_addresses,
                                               find_customer_cities_without_stores,
                                               check_if_employee_is_employed_and_how_long)

with Session() as session:
    #stmt = customer_by_name('William')
    #customers = session.scalars(stmt).all()
    #print(customers)
    rows = session.execute(check_if_employee_is_employed_and_how_long()).all()

data = [dict(row._mapping) for row in rows]
#
file_handler = FileHandler()
file_handler.write_file(data, './dump/employees_status.json')