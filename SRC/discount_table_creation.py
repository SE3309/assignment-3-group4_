from faker import Faker
import random
import csv
import sqlite3
import pandas as pd

faker = Faker('en_CA')

numRecords = 10

outputFile = 'SRC/discount_data.csv'

with open(outputFile, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['discountID', 'discountCode', 'percentage'])

    for i in range(1, numRecords + 1):
        discountID = f"D{i:03d}"
        discountCode = f"DIS{random.randint(1000, 9999)}"
        percentage = i*5
        writer.writerow([discountID, discountCode, percentage])
    
print(f"Generated {numRecords} records in {outputFile}")

df = pd.read_csv(outputFile)
conn = sqlite3.connect('SRC/StorageRoomManagement.db')
df.to_sql('Discount', conn, if_exists='replace', index=False)
conn.close()
print("Data imported into SQLite database 'SRC/StorageRoomManagement.db' in table 'Discount'")