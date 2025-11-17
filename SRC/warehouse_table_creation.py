from faker import Faker
import random
import csv
import sqlite3
import pandas as pd

faker = Faker('en_CA')

numRecords = 10

outputFile = 'SRC/warehouse_data.csv'

conn = sqlite3.connect('SRC/StorageRoomManagement.db')
cursor = conn.cursor()
cursor.execute("SELECT postalCode FROM PostalArea")
postal_codes = [row[0] for row in cursor.fetchall()]
conn.close()

with open(outputFile, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['warehouseID', 'street', 'postalCode'])

    for i in range(1, numRecords + 1):
        warehouseID = f"W{i:03d}"
        street = faker.street_address()
        postalCode = random.choice(postal_codes)
        writer.writerow([warehouseID, street, postalCode])
    
print(f"Generated {numRecords} records in {outputFile}")

df = pd.read_csv(outputFile)
conn = sqlite3.connect('SRC/StorageRoomManagement.db')
df.to_sql('Warehouse', conn, if_exists='replace', index=False)
conn.close()
print(f"Data inserted into SQLite database 'SRC/StorageRoomManagement.db' in table 'Warehouse'")