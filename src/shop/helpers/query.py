from src.shop.db.session import Session
from src.shop.queries.product_queries import *
from src.shop.queries.order_queries import *
from src.shop.queries.customer_queries import *
from src.shop.queries.employee_queries import *

from src.shop.handlers.file_handler import FileHandler

QUERIES ={
    "find_product_names_longer_than_50_characters": lambda s: s.execute(find_product_names_longer_than_50_characters()).all(),
    "show_products_cheaper_than_300_and_more_expensive_than_2000": lambda s: s.execute(show_products_cheaper_than_300_and_more_expensive_than_2000()).all(),
    "count_duplicated_orders": lambda s: s.execute(count_duplicated_orders()).all(),
    "count_orders_with_at_least_51_items_by_employees": lambda s: s.execute(count_orders_with_at_least_51_items_by_employees()).all(),
    "select_customer_who_is_worker": lambda s: s.execute(select_customer_who_is_worker()).all(),
    "find_customers_that_made_orders_in_2017": lambda s: s.execute(find_customers_that_made_orders_in_2017()).all(),
    "count_total_sales_per_month": lambda s: s.execute(count_total_sales_per_month()).all(),
    "count_products_ordered_less_than_1100": lambda s: s.execute(count_products_ordered_less_than_1100()).all(),
    "avg_days_to_complete_order": lambda s: s.execute(avg_days_to_complete_order()).all(),
    "top10_percent_products": lambda s: s.execute(top10_percent_products()).all(),
    "sales_per_product_name_sales_per_category": lambda s: s.execute(sales_per_product_name_sales_per_category()).mappings().all(),
    "show_all_employees_names": lambda s: s.execute(show_all_employees_names()).mappings().all(),
    "customers_and_their_addresses": lambda s: s.execute(customers_and_their_addresses()).mappings().all(),
    "get_employee_and_sales_sum_in_2022_2023": lambda s: s.execute(get_employee_and_sales_sum_in_2022_2023()).mappings().all(),
    "product_price_and_rank": lambda s: s.execute(product_price_and_rank()).mappings().all(),
    "select_top_5_products_info": lambda s: s.execute(select_top_5_products_info()).mappings().all(),
    "count_products_within_category": lambda s: s.execute(count_products_within_category()).mappings().all()
}

def run(query_name: str):
    if query_name not in QUERIES:
        raise ValueError(f"Invalid query name: {query_name}")

    with Session() as session:
        return QUERIES[query_name](session)

if __name__ == "__main__":
    file_handler = FileHandler()

    query_and_filename = "count_products_within_category"

    result = run(query_and_filename)
    data = [dict(row) for row in result]

    file_handler.write_file(data, f'./dump/{query_and_filename}.json')


