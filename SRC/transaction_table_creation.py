from faker import Faker #this is the main library used to generate fake data
import random
import csv
import sqlite3  #to interact with SQLite database
import pandas as pd #to handle dataframes and CSV files

fake = Faker('en_CA')

numRecords = 3000   #number of transaction records to generate, now there are 3 tables with more than a thousand records each
outputFile = 'SRC/transactions_data.csv'

paymentTypes = ['Credit Card', 'Debit Card', 'Mobile Payment', 'Bank Transfer']  #possible payment types

conn = sqlite3.connect('SRC/StorageRoomManagement.db')
cursor = conn.cursor()
cursor.execute("SELECT email FROM Customer")    #fetch all customer emails from Customer table
customerEmails = [row[0] for row in cursor.fetchall()]
conn.close()


existing_transactionIDs = set()  #to keep track of unique transaction IDs

def generate_transactionID(index):  #generate unique transaction IDs
    while True:
        transactionID = f"TR{index:05d}"
        if transactionID not in existing_transactionIDs:
            existing_transactionIDs.add(transactionID)
            return transactionID
        index += 1

def generate_raw_data():    #generate raw transaction data
    transactionID = generate_transactionID(len(existing_transactionIDs) + 1)
    amount = round(random.uniform(1000.0, 5000.0), 2)

    paymentType = random.choice(paymentTypes)

    
    if paymentType in ['Credit Card', 'Debit Card']:
        paymentDetails = fake.credit_card_number()  #generate fake credit/debit card number
    elif paymentType == 'Mobile Payment':
        paymentDetails = fake.iban()  #generate fake IBAN for mobile payment
    else:
        paymentDetails = fake.swift()  #generate fake SWIFT code for bank transfer
    transactionDate = fake.date_between(start_date='-1y', end_date='today')  #generate a transaction date within the last year
    transactionStatus = random.choice(['Completed', 'Pending', 'Failed'])  #randomly choose a transaction status

    email = random.choice(customerEmails)   #associate the transaction with a random customer email

    return [
        transactionID,
        amount,
        paymentType,
        paymentDetails,
        transactionDate,
        transactionStatus,
        email
    ]



with open(outputFile, mode='w', newline='') as file:    #write the generated data to a CSV file
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



df = pd.read_csv(outputFile)    #read the generated CSV file into a DataFrame
conn = sqlite3.connect('SRC/StorageRoomManagement.db')
df.to_sql('Transactions', conn, if_exists='replace', index=False)
conn.close()

print("Data imported into SQLite database 'SRC/StorageRoomManagement.db' in table 'Transaction'")