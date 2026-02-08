from src.shop.db.session import Session
from src.shop.queries.product_queries import *
from src.shop.queries.order_queries import *
from src.shop.queries.customer_queries import *

from src.shop.handlers.file_handler import FileHandler

QUERIES ={
    "find_product_names_longer_than_50_characters": lambda s: s.execute(find_product_names_longer_than_50_characters()).all(),
    "show_products_cheaper_than_300_and_more_expensive_than_2000": lambda s: s.execute(show_products_cheaper_than_300_and_more_expensive_than_2000()).all(),
    "count_duplicated_orders": lambda s: s.execute(count_duplicated_orders()).all(),
    "count_orders_with_at_least_51_items_by_employees": lambda s: s.execute(count_orders_with_at_least_51_items_by_employees()).all(),
    "select_customer_who_is_worker": lambda s: s.execute(select_customer_who_is_worker()).all(),
    "find_customers_that_made_orders_in_2017": lambda s: s.execute(find_customers_that_made_orders_in_2017()).all(),
    "count_total_sales_per_month": lambda s: s.execute(count_total_sales_per_month()).all()
}

def run(query_name: str):
    if query_name not in QUERIES:
        raise ValueError(f"Invalid query name: {query_name}")

    with Session() as session:
        return QUERIES[query_name](session)

if __name__ == "__main__":
    file_handler = FileHandler()

    #result = run("find_product_names_longer_than_50_characters")
    #result2 = run("count_orders_with_at_least_51_items_by_employees")
    result3=run("count_total_sales_per_month")
    file_handler.write_file(result3, './dump/sales_per_month.json')


