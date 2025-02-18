import psycopg2
import pandas as pd

database = "harvard_db"
username = "team5admin"
password = "p6dNsrbjDJHwcth6J7s2"
hostname = "database-ads507.covo6ogaonsd.us-east-1.rds.amazonaws.com"

connection = psycopg2.connect(database=database, user=username, password=password, host=hostname, port=5432)
connection.autocommit = True
cursor = connection.cursor()

# Reading Data from CSV
file_p = '/Users/katherinekimberling/ADS507_FinalProject/product_hs92.csv'
data = pd.read_csv(file_p)
print(data.head())

# Drop the table if it exists
cursor.execute('''DROP TABLE IF EXISTS "product" CASCADE;''')
connection.commit()

# Create a product table in PostgreSQL
create_table_query = '''
CREATE TABLE IF NOT EXISTS product (
    product_id INT,
    product_code TEXT,
    product_name VARCHAR(255),
    product_level INT,
    top_parent_id INT,
    product_hierarchy TEXT,
    PRIMARY KEY (product_id)
);
'''
cursor.execute(create_table_query)
connection.commit()

# Populate the table with the data
populate_product_query = '''
INSERT INTO product(product_id, product_code, product_name, product_level, top_parent_id, product_hierarchy)
VALUES (%s, %s, %s, %s, %s, %s);
'''

for _, row in data.iterrows():
    cursor.execute(populate_product_query, tuple(row))
connection.commit()

# Verifying Data Migration
populate_verify = '''SELECT * FROM product WHERE product_id < 50;'''
cursor.execute(populate_verify)
rows = cursor.fetchall()
for row in rows:
    print(row)

# Query to get column names and types
table_name = 'product'
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
