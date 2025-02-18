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
dta_file_path = '/Users/katherinekimberling/ADS507_FinalProject/services_unilateral_country_product_year_1.dta'
df = pd.read_stata(dta_file_path)

# Save as .csv
csv_file_path = '/Users/katherinekimberling/ADS507_FinalProject/services_unilateral_country_product_year_1.csv'
df.to_csv(csv_file_path)

# Reading Data from CSV
file_s1 = '/Users/katherinekimberling/ADS507_FinalProject/services_unilateral_country_product_year_1.csv'
data = pd.read_csv(file_s1)
print(data.head())

# Drop the table if it exists
cursor.execute('''DROP TABLE IF EXISTS "services_1" CASCADE;''')
connection.commit()

# Create a services_1 table in PostgreSQL
create_svs1_query = '''
CREATE TABLE IF NOT EXISTS services_1 (
    record_number INT NOT NULL,
    country_id INT,
    product_id INT,
    year INT,
    export_value FLOAT,
    import_value FLOAT,
    global_market_share FLOAT,
    PRIMARY KEY (record_number)
);
'''
cursor.execute(create_svs1_query)
connection.commit()

# Populate the table with the data
services_1_query = '''
INSERT INTO services_1(record_number, country_id, product_id, year, export_value, import_value, global_market_share)
VALUES (%s, %s, %s, %s, %s, %s, %s);
'''

for _, row in data.iterrows(): 
    cursor.execute(services_1_query, tuple(row))
connection.commit()

#Add empty pci column to make all services tables cohesive and match
add_column_query = '''
ALTER TABLE services_1
    ADD COLUMN pci INT NULL;'''
cursor.execute(add_column_query)
connection.commit()

#Create foreign key constraints for services1 with country table and product table
svs1_fk_country = '''
ALTER TABLE services_1
    ADD CONSTRAINT fk_country
    FOREIGN KEY (country_id)
    REFERENCES country(country_id);
    '''
cursor.execute(svs1_fk_country)
connection.commit()

svs1_fk_product = '''
ALTER TABLE services_1
    ADD CONSTRAINT fk_product
    FOREIGN KEY (product_id)
    REFERENCES product(product_id);
    '''
cursor.execute(svs1_fk_product)
connection.commit()

# Verifying Data Migration
populate_verify = '''SELECT record_number, year, country_id FROM services_1 WHERE record_number < 87;'''
cursor.execute(populate_verify)
rows = cursor.fetchall()
for row in rows:
    print(row)

# Query to get column names and types
table_name = 'services_1'
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
