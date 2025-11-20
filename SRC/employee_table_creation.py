from faker import Faker #this is the main library used to generate fake data
import random
import csv
import sqlite3  #to interact with SQLite database
import pandas as pd #to handle dataframes and CSV files

fake = Faker('en_CA')

numRecords = 300    #number of employee records to generate
outputFile = 'SRC/employee_data.csv'    #output CSV file path

existing_emails = set() #to keep track of unique emails
existing_employeeIDs = set()    #to keep track of unique employee IDs

conn = sqlite3.connect('SRC/StorageRoomManagement.db')  #connect to the SQLite database and it is named StorageRoomManagement.db
cursor = conn.cursor()
cursor.execute("SELECT warehouseID FROM Warehouse") #fetch all warehouse IDs from Warehouse table
warehouseIDs = [row[0] for row in cursor.fetchall()]
conn.close()


def generate_unique_email(firstName, lastName): #generate unique email addresses like customers
    while True:
        domain = fake.free_email_domain()
        email = f"{firstName.lower()}.{lastName.lower()}{random.randint(1,9999)}@{domain}"
        if email not in existing_emails:
            existing_emails.add(email)
            return email
        
def generate_phone_number():    #generate phone numbers
    return f"+1 ({random.randint(200, 999)}) {random.randint(100, 999)}-{random.randint(1000, 9999)}"

def generate_employeeID(index): #generate unique employee IDs
    while True:
        employeeID = f"SMS{index:05d}"
        if employeeID not in existing_employeeIDs:
            existing_employeeIDs.add(employeeID)
            return employeeID
        index += 1

def generate_raw_data():    #generate raw data for each employee
    employeeID = generate_employeeID(len(existing_employeeIDs) + 1)
    firstName = fake.first_name()
    lastName = fake.last_name()
    phoneNo = generate_phone_number()
    email = generate_unique_email(firstName, lastName)
    if random.random() < 0.2:   #20% chance of being Maintenance
        empRole = 'Maintenance'
    else:
        empRole = 'Staff'   #80% chance of being Staff
    warehouseID = random.choice(warehouseIDs)
    
    return [employeeID, firstName, lastName, phoneNo, email, empRole, warehouseID]

def generate_manager_data(index):   #generate manager data
    employeeID = generate_employeeID(len(existing_employeeIDs) + 1)
    firstName = fake.first_name()
    lastName = fake.last_name()
    phoneNo = generate_phone_number()
    email = generate_unique_email(firstName, lastName)
    warehouseID = warehouseIDs[index]
    empRole = 'Manager'
    return [employeeID, firstName, lastName, phoneNo, email, empRole, warehouseID]

def generate_supervisor_data(index):    #generate supervisor data
    employeeID = generate_employeeID(len(existing_employeeIDs) + 1)
    firstName = fake.first_name()
    lastName = fake.last_name()
    phoneNo = generate_phone_number()
    email = generate_unique_email(firstName, lastName)
    warehouseID = warehouseIDs[index]
    empRole = 'Supervisor'
    return [employeeID, firstName, lastName, phoneNo, email, empRole, warehouseID]

with open(outputFile, mode='w', newline='') as file:    #write employee data to CSV file
    writer = csv.writer(file)
    writer.writerow(['employeeID', 'firstName', 'lastName', 'phoneNo', 'email', 'empRole', 'warehouseID'])

    for i in range(0, len(warehouseIDs)):   #generate manager data
        employeeID, firstName, lastName, phoneNo, email, empRole, warehouseID = generate_manager_data(i)

        writer.writerow([employeeID, firstName, lastName, phoneNo, email, empRole, warehouseID])

    for i in range(0, len(warehouseIDs)):   #generate supervisor data
        employeeID, firstName, lastName, phoneNo, email, empRole, warehouseID = generate_supervisor_data(i)
        writer.writerow([employeeID, firstName, lastName, phoneNo, email, empRole, warehouseID])
        employeeID, firstName, lastName, phoneNo, email, empRole, warehouseID = generate_supervisor_data(i)
        writer.writerow([employeeID, firstName, lastName, phoneNo, email, empRole, warehouseID])

    for i in range(1, numRecords - 2 * len(warehouseIDs) + 1):
        employeeID, firstName, lastName, phoneNo, email, empRole, warehouseID = generate_raw_data()  #generate regular employee data
        writer.writerow([employeeID, firstName, lastName, phoneNo, email, empRole, warehouseID])

print(f"Generated {numRecords} records in {outputFile}")


df = pd.read_csv(outputFile)
conn = sqlite3.connect('SRC/StorageRoomManagement.db')  #connect to the SQLite database named StorageRoomManagement.db
df.to_sql('Employee', conn, if_exists='replace', index=False)
conn.close()
print("Data imported into SQLite database 'SRC/StorageRoomManagement.db' in table 'Employee'")