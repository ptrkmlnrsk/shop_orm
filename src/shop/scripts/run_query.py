from typing import TYPE_CHECKING
from src.shop.db.session import Session
from src.shop.models import Customer
from src.shop.scripts.file_handler import FileHandler

from src.shop.queries.customer_queries import (customer_by_name,
                                               customers_and_their_addresses,
                                               find_customer_cities_without_stores,
                                               check_if_employee_is_employed_and_how_long,
                                               find_product_names_longer_than_50_characters,
                                               calculate_ratio_discounted_to_non_discounted_products)

with Session() as session:
    #stmt = customer_by_name('William')
    #customers = session.scalars(stmt).all()
    #print(customers)
    #rows = find_product_names_longer_than_50_characters()
    stmt = calculate_ratio_discounted_to_non_discounted_products()
    discounted, non_discounted = session.execute(stmt).one()

print(discounted, non_discounted)
#data = [dict(row._mapping) for row in rows]
#print(data)
##
#file_handler = FileHandler()
#file_handler.write_file(data, './dump/employees_status.json')