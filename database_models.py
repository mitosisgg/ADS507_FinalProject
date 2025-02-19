from fastapi import BackgroundTasks
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, BigInteger, Text, Double, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

import asyncio
import os
import pandas as pd


# Database connection with explicit credentials
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("DB_NAME")

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:5432/{DB_NAME}"
print(f'DATABASE_URL: {DATABASE_URL}')

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Creates the tables in the database
def create_tables():
    metadata = MetaData()

    # `Product` Table definition
    product_table = Table('product', metadata,
        Column('product_id', BigInteger),
        Column('code', Text, primary_key=True),
        Column('name_short_en', Text),
        Column('product_level', BigInteger),
        Column('top_parent_id', BigInteger),
        Column('product_id_hierarchy', Text),
    )

    # `Country` Table definition
    country_table = Table('country', metadata,
        Column('country_id', BigInteger, primary_key=True),
        Column('name_short_en', Text),
        Column('iso3_code', Text),
        Column('legacy_location_id', BigInteger)
    )

    # `Service` Table definition
    service_table = Table('service', metadata,
        Column('service_id', BigInteger),
        Column('country_id', Integer),
        Column('product_id', Integer),
        Column('year', Integer),
        Column('export_value', Double),
        Column('import_value', Double),
        Column('global_market_share', Double)
    )

    # Drop tables if they exist
    print('Dropping tables if they exist...')
    metadata.drop_all(engine, checkfirst=True)

    print('Creating tables product, country, service')
    # Create the table in the database
    metadata.create_all(engine)

# Inserts data into tables
async def seed_database():
    print('Inserting data into tables...')

    # COUNTRY
    print('Inserting into country')
    countries = pd.read_csv('./harvard_trade_data/location_country.csv')
    countries.to_sql('country', con=engine, if_exists='append', index=False)

    # PRODUCT
    print('Inserting into product')
    products = pd.read_csv('./harvard_trade_data/product_hs92.csv')
    products.to_sql('product', con=engine, if_exists='append', index=False)

    # SERVICES
    print('Inserting into service')
    services1 = pd.read_stata('./harvard_trade_data/services_unilateral_country_product_year_1.dta')
    services2 = pd.read_stata('./harvard_trade_data/services_unilateral_country_product_year_2.dta')
    services3 = pd.read_stata('./harvard_trade_data/services_unilateral_country_product_year_4.dta')
    services4 = pd.read_stata('./harvard_trade_data/services_unilateral_country_product_year_6.dta')

    services = pd.concat([services1, services2, services3, services4])   # union services dataframes
    services.drop(columns=['pci'], inplace=True) # drop column 'pci'
    services = services.sort_values(by='year') # make chronological order'

    # Insert .5% of the services dataframe into the db every 10 seconds
    chunk_size = len(services) // 100
    for start in range(0, len(services), chunk_size):
        print('Inserting Chunk {}:{}'.format(start, start + chunk_size))
        end = start + chunk_size
        try:
            services_chunk = services.iloc[start:end]
            services_chunk.to_sql('service', con=engine, if_exists='append', index=True, index_label='service_id')
        except Exception as e:
            print(f'Error inserting chunk: {e}')
        await asyncio.sleep(1)
    print('Database initilization complete')

# Database initialization function
def init_db():
    create_tables()
    Base.metadata.create_all(bind=engine)

# Database session dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()