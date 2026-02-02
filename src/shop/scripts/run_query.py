from src.shop.db.session import Session

from src.shop.queries.customer_queries import (find_customer_cities_without_stores,
                                               check_if_employee_is_employed_and_how_long,
                                               find_product_names_longer_than_50_characters,
                                               calculate_ratio_discounted_to_non_discounted_products,
                                               calculate_min_max_client_spent)

with Session() as session:
    #stmt = customer_by_name('William')
    #customers = session.scalars(stmt).all()
    #print(customers)
    #rows = find_product_names_longer_than_50_characters()
    #stmt = calculate_ratio_discounted_to_non_discounted_products()
    #discounted, non_discounted = session.execute(stmt).one()
    stmt = calculate_min_max_client_spent()
    session.execute(stmt)

#print(discounted, non_discounted)
#data = [dict(row._mapping) for row in rows]
#print(data)
##
#file_handler = FileHandler()
#file_handler.write_file(data, './dump/employees_status.json')