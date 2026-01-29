import sqlalchemy as sa
from src.shop.config import DATABASE_URL

connection_url = sa.engine.URL.create(
    "mssql+pyodbc",
    host="localhost",
    port=1433,
    database="master",
    query={"driver": "ODBC Driver 18 for SQL Server", "Encrypt": "no"}
)
print(DATABASE_URL)
print(connection_url)

engine = sa.create_engine(
    DATABASE_URL,
    echo=True)
