from faker import Faker
import random
import csv
import sqlite3
import pandas as pd

fake = Faker('en_CA')

numRecords = 500
outputFile = 'SRC/postalArea_data.csv'

existing_postal_codes = set()

def generate_city_postal_code():
    while True:
        postalCode = fake.postalcode()
        city = fake.city()
        if postalCode not in existing_postal_codes:
            existing_postal_codes.add(postalCode)
            return postalCode, city


with open(outputFile, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['postalCode', 'city'])

    for i in range(numRecords):
        postalCode, city = generate_city_postal_code()
        writer.writerow([postalCode, city])

print(f"Generated {numRecords} records in {outputFile}")

df = pd.read_csv(outputFile)
conn = sqlite3.connect('SRC/StorageRoomManagement.db')
df.to_sql('PostalArea', conn, if_exists='replace', index=False)
conn.close()
print(f"Data inserted into SQLite database 'SRC/StorageRoomManagement.db' in table 'PostalArea'")