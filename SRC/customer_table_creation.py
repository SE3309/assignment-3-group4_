from faker import Faker
import random
import csv
import sqlite3
import pandas as pd

fake = Faker('en_CA')

numRecords = 2500
outputFile = 'SRC/customer_data.csv'

conn = sqlite3.connect('SRC/StorageRoomManagement.db')
cursor = conn.cursor()
cursor.execute("SELECT postalCode FROM PostalArea")
postal_codes = [row[0] for row in cursor.fetchall()]
conn.close()

existing_emails = set()
existing_employeeIDs = set()

def generate_unique_email(firstName, lastName):
    while True:
        domain = fake.free_email_domain()
        email = f"{firstName.lower()}.{lastName.lower()}{random.randint(1,9999)}@{domain}"
        if email not in existing_emails:
            existing_emails.add(email)
            return email
        
def generate_phone_number():
    return f"+1 ({random.randint(200, 999)}) {random.randint(100, 999)}-{random.randint(1000, 9999)}"

def generate_employeeID(index):
    while True:
        employeeID = f"SMS{index:05d}"
        if employeeID not in existing_employeeIDs:
            existing_employeeIDs.add(employeeID)
            return employeeID
        index += 1

def generate_raw_data():

    firstName = fake.first_name()
    lastName = fake.last_name()
    phoneNo = generate_phone_number()
    email = generate_unique_email(firstName, lastName)
    dateOfBirth = fake.date_of_birth(minimum_age=18, maximum_age=80).strftime("%Y-%m-%d")
    street = fake.street_address()
    postal_code = random.choice(postal_codes)
    return [firstName, lastName, phoneNo, email, dateOfBirth, street, postal_code]


with open(outputFile, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['firstName', 'lastName', 'phoneNo', 'email', 'dateOfBirth', 'street', 'postal_code'])

    for i in range(1, numRecords + 1):
        firstName, lastName, phoneNo, email, dateOfBirth, street, postal_code = generate_raw_data()

        writer.writerow([firstName, lastName, phoneNo, email, dateOfBirth, street, postal_code])

print(f"Generated {numRecords} records in {outputFile}")


df = pd.read_csv(outputFile)
conn = sqlite3.connect('SRC/StorageRoomManagement.db')
df.to_sql('Customer', conn, if_exists='replace', index=False)
conn.close()
print("Data imported into SQLite database 'SRC/StorageRoomManagement.db' in table 'Customer'")