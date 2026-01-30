from typing import TYPE_CHECKING
from src.shop.db.session import Session
from src.shop.scripts.file_handler import FileHandler

from src.shop.queries.customer_queries import customer_by_name, customers_and_their_addresses

with Session() as session:
    stmt = customer_by_name('William')
    customers = session.scalars(stmt).all()

    rows = session.execute(customers_and_their_addresses()).all()

data = [dict(row._mapping) for row in rows]

file_handler = FileHandler()
file_handler.write_file(data, './dump/exported_customer_data.json')