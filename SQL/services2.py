import psycopg2
import pandas as pd

database = "harvard_db"
username = "team5admin"
password = "p6dNsrbjDJHwcth6J7s2"
hostname = "database-ads507.covo6ogaonsd.us-east-1.rds.amazonaws.com"

connection = psycopg2.connect(database=database, user=username, password=password, host=hostname, port=5432)
cursor = connection.cursor()

# Converting source data files from .dta to .csv format
# Load the .dta file
dta_file_path = '/Users/katherinekimberling/ADS507_FinalProject/services_unilateral_country_product_year_2.dta'
df = pd.read_stata(dta_file_path)

# Save as .csv
csv_file_path = '/Users/katherinekimberling/ADS507_FinalProject/services_unilateral_country_product_year_2.csv'
df.to_csv(csv_file_path)

# Reading Data from CSV
file_s2 = '/Users/katherinekimberling/ADS507_FinalProject/services_unilateral_country_product_year_2.csv'
data = pd.read_csv(file_s2)
print(data.head())

# Drop the table if it exists
cursor.execute('''DROP TABLE IF EXISTS "services_2" CASCADE;''')
connection.commit()

# Create a services_2 table in PostgreSQL
create_svs2_query = '''
CREATE TABLE IF NOT EXISTS services_2 (
    record_number INT,
    country_id INT,
    product_id INT,
    year INT,
    export_value FLOAT,
    import_value FLOAT,
    global_market_share FLOAT,
    PRIMARY KEY (record_number)
);
'''
cursor.execute(create_svs2_query)
connection.commit()

# Populate the table with the data
services_2_query = '''
INSERT INTO services_2(record_number, country_id, product_id, year, export_value, import_value, global_market_share)
VALUES (%s, %s, %s, %s, %s, %s, %s);
'''

for _, row in data.iterrows():
    cursor.execute(services_2_query, tuple(row))
connection.commit()

#Add empty pci column to make all services tables cohesive and match
alter_svs2_query = '''
ALTER TABLE services_2
    ADD COLUMN pci INT NULL;'''
cursor.execute(alter_svs2_query)
connection.commit()


#Create foreign key constraints for services2 with country table and product table
svs2_fk_country = '''
ALTER TABLE services_2
    ADD CONSTRAINT fk_country
    FOREIGN KEY (country_id)
    REFERENCES country(country_id);
'''
cursor.execute(svs2_fk_country)
connection.commit()

svs2_fk_product = '''
ALTER TABLE services_2
    ADD CONSTRAINT fk_product
    FOREIGN KEY (product_id)
    REFERENCES product(product_id);'''
cursor.execute(svs2_fk_product)
connection.commit()

# Verifying Data Migration
populate_verify = '''SELECT COUNT(DISTINT record_number) FROM services_2;'''
cursor.execute(populate_verify)
rows = cursor.fetchall()
for row in rows:
    print(row)

# Query to get column names and types
table_name = 'services_2'
cursor.execute(f"SELECT column_name, data_type FROM information_schema.columns WHERE table_name = '{table_name}'")

# Fetch all results
columns = cursor.fetchall()

# Display column names and types
print("Column Name\t\tColumn Type")
print("-" * 40)
for column in columns:
    print(f"{column[0]}\t\t{column[1]}")

# Close the cursor and connection
cursor.close()
connection.close()
