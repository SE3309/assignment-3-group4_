from faker import Faker #this is the main library used to generate fake data
import random
import csv
import sqlite3  #to interact with SQLite database
import pandas as pd #to handle dataframes and CSV files

fake = Faker('en_CA')   #initialize Faker with Canadian English locale

numRecords = 500    #number of postal area records to generate
outputFile = 'SRC/postalArea_data.csv'  #output CSV file path

existing_postal_codes = set()   #to keep track of unique postal codes

def generate_city_postal_code():    #generate unique postal codes and corresponding cities
    while True:
        postalCode = fake.postalcode()
        city = fake.city()
        if postalCode not in existing_postal_codes:
            existing_postal_codes.add(postalCode)
            return postalCode, city


with open(outputFile, mode='w', newline='') as file:    #write the generated data to a CSV file
    writer = csv.writer(file)
    writer.writerow(['postalCode', 'city'])

    for i in range(numRecords):
        postalCode, city = generate_city_postal_code()
        writer.writerow([postalCode, city])

print(f"Generated {numRecords} records in {outputFile}")

df = pd.read_csv(outputFile)    #read the generated CSV file into a DataFrame
conn = sqlite3.connect('SRC/StorageRoomManagement.db')  #connect to the SQLite database and it is named StorageRoomManagement.db
df.to_sql('PostalArea', conn, if_exists='replace', index=False)
conn.close()
print(f"Data inserted into SQLite database 'SRC/StorageRoomManagement.db' in table 'PostalArea'")