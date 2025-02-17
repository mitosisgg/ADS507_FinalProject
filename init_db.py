import os
import pandas as pd

from dotenv import load_dotenv
from sqlalchemy import create_engine

# ENVIRONMENT VARS
load_dotenv()
DB_HOST = os.getenv("DB_HOST")
DB_USERNAME = os.getenv("DB_USERNAME")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")

# COUNTRY
countries = pd.read_csv('./harvard_trade_data/location_country.csv')

# PRODUCT
products = pd.read_csv('./harvard_trade_data/product_hs92.csv')

# SERVICES
services1 = pd.read_stata('./harvard_trade_data/services_unilateral_country_product_year_1.dta')
services2 = pd.read_stata('./harvard_trade_data/services_unilateral_country_product_year_2.dta')
services3 = pd.read_stata('./harvard_trade_data/services_unilateral_country_product_year_4.dta')
services4 = pd.read_stata('./harvard_trade_data/services_unilateral_country_product_year_6.dta')

services = pd.concat([services1, services2, services3, services4])   # union services dataframes


# Create connection to remote db (aws)
conn_url = f'postgresql://{os.getenv("DB_USER")}:{os.getenv("DB_PASSWORD")}@{os.getenv("DB_HOST")}/{os.getenv("DB_NAME")}'
engine = create_engine(conn_url)

# Commit to db
countries.to_sql('country_test', con=engine, if_exists='replace', index=False)
products.to_sql('product_test', con=engine, if_exists='replace', index=False)
services.to_sql('services_test', con=engine, if_exists='replace', index=False)