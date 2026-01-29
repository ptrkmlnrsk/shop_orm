from typing import TYPE_CHECKING
from src.shop.db.session import Session

from src.shop.queries.customer_queries import customer_by_name

with Session() as session:
    stmt = customer_by_name('William')
    rows = session.scalars(stmt).one()
    print(rows)
    for r in rows:
        print(r.customer_id, r.first_name, r.last_name, r.phone_number, r.email)