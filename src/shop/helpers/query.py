from src.shop.db.session import Session
from src.shop.queries.product_queries import *

from src.shop.handlers.file_handler import FileHandler

QUERIES ={
    "find_product_names_longer_than_50_characters": lambda s: s.execute(find_product_names_longer_than_50_characters()).all(),
    "show_products_cheaper_than_300_and_more_expensive_than_2000": lambda s: s.execute(show_products_cheaper_than_300_and_more_expensive_than_2000()).all()
}

def run(query_name: str):
    if query_name not in QUERIES:
        raise ValueError(f"Invalid query name: {query_name}")

    with Session() as session:
        return QUERIES[query_name](session)

if __name__ == "__main__":
    file_handler = FileHandler()

    #result = run("find_product_names_longer_than_50_characters")
    result2 = run("show_products_cheaper_than_300_and_more_expensive_than_2000")
    file_handler.write_file(result2, './dump/products_cheaper_than_300_and_more_expensive_than_2000.json')

    print(result2)

