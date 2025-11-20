from faker import Faker #this is the main library used to generate fake data
import random
import csv
import sqlite3  #to interact with SQLite database
import pandas as pd #to handle dataframes and CSV files

faker = Faker('en_CA')  #initialize Faker for Canadian locale

numRecords = 10   #number of warehouse records to generate, there are only 10 warehouses

outputFile = 'SRC/warehouse_data.csv'

conn = sqlite3.connect('SRC/StorageRoomManagement.db')
cursor = conn.cursor()
cursor.execute("SELECT postalCode FROM PostalArea") #fetch all postal codes from PostalArea table
postal_codes = [row[0] for row in cursor.fetchall()]
conn.close()

with open(outputFile, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['warehouseID', 'street', 'postalCode'])  #write header row to CSV file

    for i in range(1, numRecords + 1):
        warehouseID = f"W{i:03d}"   #generate warehouse ID with leading zeros
        street = faker.street_address() #generate fake street address
        postalCode = random.choice(postal_codes)    #randomly select a postal code from existing postal codes
        writer.writerow([warehouseID, street, postalCode])
    
print(f"Generated {numRecords} records in {outputFile}")

df = pd.read_csv(outputFile)    #read the generated CSV file into a DataFrame
conn = sqlite3.connect('SRC/StorageRoomManagement.db')  #connect to the SQLite database and it is named StorageRoomManagement.db
df.to_sql('Warehouse', conn, if_exists='replace', index=False)
conn.close()
print(f"Data inserted into SQLite database 'SRC/StorageRoomManagement.db' in table 'Warehouse'")