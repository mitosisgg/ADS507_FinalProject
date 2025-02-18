import psycopg2
import pandas as pd

database = "harvard_db"
username = "DB_USER"
password = "DB_PASSWORD"
hostname = "database-ads507.covo6ogaonsd.us-east-1.rds.amazonaws.com"

connection = psycopg2.connect(database=database, user=username, password=password, host=hostname, port=5432)
connection.autocommit = True
cursor = connection.cursor()

# Reading Data from CSV
file_c = '/Users/katherinekimberling/ADS507_FinalProject/location_country.csv'
data = pd.read_csv(file_c)
print(data.head())

# Drop the table if it exists
cursor.execute('''DROP TABLE IF EXISTS "country" CASCADE;''')
connection.commit()

# Create a country Table in PostgreSQL
create_table_query = '''
CREATE TABLE IF NOT EXISTS country (
    country_id INT,
    name_short_en VARCHAR(200),
    iso3_code VARCHAR(3),
    legacy_location_id INT,
    PRIMARY KEY (country_id)
);
'''
cursor.execute(create_table_query)
connection.commit()

# Populate the table with the data
populate_country_query = '''
INSERT INTO country(country_id, name_short_en, iso3_code, legacy_location_id)
VALUES (%s, %s, %s, %s);
'''

for _, row in data.iterrows():
    cursor.execute(populate_country_query, tuple(row))
connection.commit()

# Verifying Data Migration
populate_query = '''SELECT * FROM country WHERE legacy_location_id < 50;'''
cursor.execute(populate_query)
rows = cursor.fetchall()
for row in rows:
    print(row)

# Query to get column names and types
table_name = 'country'
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
