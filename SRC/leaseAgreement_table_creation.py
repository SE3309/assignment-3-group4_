from faker import Faker #this is the main library used to generate fake data
import random
import csv
import sqlite3  #to interact with SQLite database
import pandas as pd #to handle dataframes and CSV files

fake = Faker('en_CA')   #initialize Faker with Canadian English locale

numRecords = 3000   #number of lease agreement records to generate
outputFile = 'SRC/leaseAgreement_data.csv'  #output CSV file path

conditions = ['Climate Controlled', 'Multipurpose', 'Multiple Access', 'Standard', 'Vehicle Storage']   #possible lease conditions


conn = sqlite3.connect('SRC/StorageRoomManagement.db')  #connect to the SQLite database and it is named StorageRoomManagement.db
cursor = conn.cursor()
cursor.execute("SELECT email FROM Customer")        #fetch all customer emails from Customer table
customerEmails = [row[0] for row in cursor.fetchall()]
cursor.execute("SELECT transactionID FROM Transactions")   #fetch all transaction IDs from Transactions table
transactionIDs = [row[0] for row in cursor.fetchall()]
cursor.execute("SELECT discountID FROM Discount")   #fetch all discount IDs from Discount table
discountIDs = [row[0] for row in cursor.fetchall()]
conn.close()


existing_leaseIDs = set()   #to keep track of unique lease IDs

def generate_leaseID(index):    #generate unique lease IDs
    while True:
        leaseID = f"L{index:05d}"
        if leaseID not in existing_leaseIDs:
            existing_leaseIDs.add(leaseID)
            return leaseID
        index += 1

def generate_raw_data():    #generate raw lease agreement data
    leaseID = generate_leaseID(len(existing_leaseIDs) + 1)

    
    startDate = fake.date_between(start_date='-2y', end_date='today')
    endDate = fake.date_between(start_date=startDate, end_date='+2y')
    leaseCondition = random.choice(conditions)    
    emailAddress = random.choice(customerEmails)
    transactionID = random.choice(transactionIDs)
    discountID = random.choice(discountIDs) if random.random() >= 0.8 else 'NULL'   #20% chance of having a discountID

    return [
        leaseID,
        startDate,
        endDate,
        leaseCondition,
        emailAddress,
        transactionID,
        discountID
    ]


with open(outputFile, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow([
        'leaseID',
        'startDate',
        'endDate',
        'leaseCondition',
        'email',
        'transactionID',
        'discountID'
    ])

    for i in range(1, numRecords + 1):
        writer.writerow(generate_raw_data())

print(f"Generated {numRecords} records in {outputFile}")


df = pd.read_csv(outputFile)    #read the generated CSV file into a DataFrame
conn = sqlite3.connect('SRC/StorageRoomManagement.db')  #connect to the SQLite database and it is named StorageRoomManagement.db
df.to_sql('LeaseAgreement', conn, if_exists='replace', index=False)
conn.close()

print("Data imported into SQLite database 'SRC/StorageRoomManagement.db' into table 'lease_agreements'") 