from faker import Faker
import random
import csv
import sqlite3
import pandas as pd

fake = Faker('en_CA')

numRecords = 3000
outputFile = 'SRC/transactions_data.csv'

paymentTypes = ['Credit Card', 'Debit Card', 'Mobile Payment', 'Bank Transfer']

conn = sqlite3.connect('SRC/StorageRoomManagement.db')
cursor = conn.cursor()
cursor.execute("SELECT email FROM Customer")
customerEmails = [row[0] for row in cursor.fetchall()]
conn.close()


existing_transactionIDs = set()

def generate_transactionID(index):
    while True:
        transactionID = f"TR{index:05d}"
        if transactionID not in existing_transactionIDs:
            existing_transactionIDs.add(transactionID)
            return transactionID
        index += 1

def generate_raw_data():
    transactionID = generate_transactionID(len(existing_transactionIDs) + 1)
    amount = round(random.uniform(1000.0, 5000.0), 2)

    paymentType = random.choice(paymentTypes)

    
    if paymentType in ['Credit Card', 'Debit Card']:
        paymentDetails = fake.credit_card_number()
    elif paymentType == 'Mobile Payment':
        paymentDetails = fake.iban()  
    else:
        paymentDetails = fake.swift()

    transactionDate = fake.date_between(start_date='-1y', end_date='today')
    transactionStatus = random.choice(['Completed', 'Pending', 'Failed'])

    email = random.choice(customerEmails)

    return [
        transactionID,
        amount,
        paymentType,
        paymentDetails,
        transactionDate,
        transactionStatus,
        email
    ]



with open(outputFile, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow([
        'transactionID',
        'amount',
        'paymentType',
        'paymentDetails',
        'transactionDate',
        'transactionStatus',
        'email'
    ])

    for _ in range(numRecords):
        writer.writerow(generate_raw_data())

print(f"Generated {numRecords} records in {outputFile}")



df = pd.read_csv(outputFile)
conn = sqlite3.connect('SRC/StorageRoomManagement.db')
df.to_sql('Transactions', conn, if_exists='replace', index=False)
conn.close()

print("Data imported into SQLite database 'SRC/StorageRoomManagement.db' in table 'Transaction'")