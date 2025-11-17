from faker import Faker
import random
import csv
import sqlite3
import pandas as pd

fake = Faker('en_CA')

numRecords = 3000
outputFile = 'SRC/leaseAgreement_data.csv'

conditions = ['Climate Controlled', 'Multipurpose', 'Multiple Access', 'Standard', 'Vehicle Storage']


conn = sqlite3.connect('SRC/StorageRoomManagement.db')
cursor = conn.cursor()
cursor.execute("SELECT email FROM Customer")
customerEmails = [row[0] for row in cursor.fetchall()]
cursor.execute("SELECT transactionID FROM Transactions")
transactionIDs = [row[0] for row in cursor.fetchall()]
cursor.execute("SELECT discountID FROM Discount")
discountIDs = [row[0] for row in cursor.fetchall()]
conn.close()


existing_leaseIDs = set()

def generate_leaseID(index):
    while True:
        leaseID = f"L{index:05d}"
        if leaseID not in existing_leaseIDs:
            existing_leaseIDs.add(leaseID)
            return leaseID
        index += 1

def generate_raw_data():
    leaseID = generate_leaseID(len(existing_leaseIDs) + 1)

    
    startDate = fake.date_between(start_date='-2y', end_date='today')
    endDate = fake.date_between(start_date=startDate, end_date='+2y')
    leaseCondition = random.choice(conditions)    
    emailAddress = random.choice(customerEmails)
    transactionID = random.choice(transactionIDs)
    discountID = random.choice(discountIDs) if random.random() >= 0.8 else 'NULL'

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


df = pd.read_csv(outputFile)
conn = sqlite3.connect('SRC/StorageRoomManagement.db')
df.to_sql('LeaseAgreement', conn, if_exists='replace', index=False)
conn.close()

print("Data imported into SQLite database 'SRC/StorageRoomManagement.db' into table 'lease_agreements'")