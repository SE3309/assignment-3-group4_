from faker import Faker
import random
import csv
import sqlite3
import pandas as pd

fake = Faker('en_CA')

numRecords = 300
outputFile = 'SRC/employee_data.csv'

existing_emails = set()
existing_employeeIDs = set()

conn = sqlite3.connect('SRC/StorageRoomManagement.db')
cursor = conn.cursor()
cursor.execute("SELECT warehouseID FROM Warehouse")
warehouseIDs = [row[0] for row in cursor.fetchall()]
conn.close()


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
    employeeID = generate_employeeID(len(existing_employeeIDs) + 1)
    firstName = fake.first_name()
    lastName = fake.last_name()
    phoneNo = generate_phone_number()
    email = generate_unique_email(firstName, lastName)
    if random.random() < 0.2:
        empRole = 'Maintenance'
    else:
        empRole = 'Staff'
    warehouseID = random.choice(warehouseIDs)
    
    return [employeeID, firstName, lastName, phoneNo, email, empRole, warehouseID]

def generate_manager_data(index):
    employeeID = generate_employeeID(len(existing_employeeIDs) + 1)
    firstName = fake.first_name()
    lastName = fake.last_name()
    phoneNo = generate_phone_number()
    email = generate_unique_email(firstName, lastName)
    warehouseID = warehouseIDs[index]
    empRole = 'Manager'
    return [employeeID, firstName, lastName, phoneNo, email, empRole, warehouseID]

def generate_supervisor_data(index):
    employeeID = generate_employeeID(len(existing_employeeIDs) + 1)
    firstName = fake.first_name()
    lastName = fake.last_name()
    phoneNo = generate_phone_number()
    email = generate_unique_email(firstName, lastName)
    warehouseID = warehouseIDs[index]
    empRole = 'Supervisor'
    return [employeeID, firstName, lastName, phoneNo, email, empRole, warehouseID]

with open(outputFile, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['employeeID', 'firstName', 'lastName', 'phoneNo', 'email', 'empRole', 'warehouseID'])

    for i in range(0, len(warehouseIDs)):
        employeeID, firstName, lastName, phoneNo, email, empRole, warehouseID = generate_manager_data(i)

        writer.writerow([employeeID, firstName, lastName, phoneNo, email, empRole, warehouseID])

    for i in range(0, len(warehouseIDs)):
        employeeID, firstName, lastName, phoneNo, email, empRole, warehouseID = generate_supervisor_data(i)
        writer.writerow([employeeID, firstName, lastName, phoneNo, email, empRole, warehouseID])
        employeeID, firstName, lastName, phoneNo, email, empRole, warehouseID = generate_supervisor_data(i)
        writer.writerow([employeeID, firstName, lastName, phoneNo, email, empRole, warehouseID])

    for i in range(1, numRecords - 2 * len(warehouseIDs) + 1):
        employeeID, firstName, lastName, phoneNo, email, empRole, warehouseID = generate_raw_data()
        writer.writerow([employeeID, firstName, lastName, phoneNo, email, empRole, warehouseID])

print(f"Generated {numRecords} records in {outputFile}")


df = pd.read_csv(outputFile)
conn = sqlite3.connect('SRC/StorageRoomManagement.db')
df.to_sql('Employee', conn, if_exists='replace', index=False)
conn.close()
print("Data imported into SQLite database 'SRC/StorageRoomManagement.db' in table 'Employee'")