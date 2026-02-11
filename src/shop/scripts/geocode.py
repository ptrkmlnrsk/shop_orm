from functools import partial

from geopy.geocoders import Nominatim
import geopandas as gpd
import pandas as pd
from src.shop.queries.customer_queries import customers_and_their_addresses
from src.shop.helpers.query import run

QUERY = {
    "customers_and_their_addresses": lambda s: s.execute(customers_and_their_addresses()).mappings().all()
}


if __name__ == "__main__":
    geolocator = Nominatim(user_agent="geocoder")
    query_name = "customers_and_their_addresses"
    result = run(query_name)
    addresses_df = pd.DataFrame([dict(row) for row in result])

    addr_col = ['street', 'city', 'country']

    addresses_df['full_address'] =(
        addresses_df['address_col']
        .fillna("")
        .astype(str)
        .agg(lambda r: ", ".join([x.strip() for x in r if x.strip()]), axis=1))


