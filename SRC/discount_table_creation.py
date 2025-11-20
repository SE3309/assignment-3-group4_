from faker import Faker #this is the main library used to generate fake data
import random
import csv
import sqlite3  #to interact with SQLite database
import pandas as pd #to handle dataframes and CSV files

faker = Faker('en_CA')  #initialize Faker for Canadian locale

numRecords = 10

outputFile = 'SRC/discount_data.csv'  #output CSV file path

with open(outputFile, mode='w', newline='') as file:    #write the generated data to a CSV file
    writer = csv.writer(file)
    writer.writerow(['discountID', 'discountCode', 'percentage'])

    for i in range(1, numRecords + 1):  #generate discount data
        discountID = f"D{i:03d}"
        discountCode = f"DIS{random.randint(1000, 9999)}"
        percentage = i*5
        writer.writerow([discountID, discountCode, percentage])
    
print(f"Generated {numRecords} records in {outputFile}")

df = pd.read_csv(outputFile)    #read the generated CSV file into a DataFrame
conn = sqlite3.connect('SRC/StorageRoomManagement.db')  #connect to the SQLite database and it is named StorageRoomManagement.db
df.to_sql('Discount', conn, if_exists='replace', index=False)
conn.close()
print("Data imported into SQLite database 'SRC/StorageRoomManagement.db' in table 'Discount'")