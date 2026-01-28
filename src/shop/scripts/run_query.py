from typing import TYPE_CHECKING
from src.shop.db.session import Session

from src.shop.queries.customer_queries import customer_by_name

with Session() as session:
    stmt = customer_by_name('Doe')
    rows = session.scalars(stmt).all
    for r in rows:
        print(r.id, r.first_name, r.last_name, r.phone_number, r.email)