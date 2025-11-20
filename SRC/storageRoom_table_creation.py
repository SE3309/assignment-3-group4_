from faker import Faker #this is the main library used to generate fake data
import random
import csv
import sqlite3  #to interact with SQLite database
import pandas as pd #to handle dataframes and CSV files

fake = Faker('en_CA')       #initialize Faker with Canadian English locale

numRecords = 500    #number of storage room records to generate
outputFile = 'SRC/storageRoom_data.csv'  #output CSV file path

storageTypes = ['Cold Storage', 'Dry Storage', 'Hazardous Materials Storage', 'General Storage', 'Bulk Storage']    #possible storage types
availabilityStatuses = ['Available', 'Occupied', 'Under Maintenance', 'Reserved']   #possible availability statuses

connect = sqlite3.connect('SRC/StorageRoomManagement.db')  #connect to the SQLite database and it is named StorageRoomManagement.db
cursor = connect.cursor()
cursor.execute("SELECT warehouseID FROM Warehouse")
warehouseIDs = [row[0] for row in cursor.fetchall()]
connect.close()

conn = sqlite3.connect('SRC/StorageRoomManagement.db')
cursor = conn.cursor()
cursor.execute("SELECT leaseID, email FROM LeaseAgreement")   #fetch all leaseIDs and corresponding emails from LeaseAgreement table
lease_data = cursor.fetchall()
lease_dict = {leaseID: email for leaseID, email in lease_data}
conn.close()

existing_storageRoomIDs = set()   #to keep track of unique storage room IDs

def generate_storageRoomID(index, warehouseID):   #generate unique storage room IDs
    while True:
        storageRoomID = f"SR{warehouseID}{index:04d}"
        if storageRoomID not in existing_storageRoomIDs:
            existing_storageRoomIDs.add(storageRoomID)
            return storageRoomID
        index += 1


with open(outputFile, mode='w', newline='') as file:    #write the generated data to a CSV file
    writer = csv.writer(file)
    writer.writerow(['roomID', 'roomNo', 'length', 'width', 'height', 'storageType', 'availabilityStatus', 'rentalPricePerDay', 'warehouseID', 'leaseID', 'email'])

    for i in range(1, numRecords + 1):
        warehouseID = random.choice(warehouseIDs)
        roomID = generate_storageRoomID(len(existing_storageRoomIDs) + 1, warehouseID)
        roomNo = f"R{random.randint(100, 999)}"
        length = round(random.uniform(5.0, 50.0), 2)   #length of the storage room in meters
        width = round(random.uniform(5.0, 50.0), 2)    #width of the storage room in meters
        height = round(random.uniform(3.0, 15.0), 2)   #height of the storage room in meters
        storageType = random.choice(storageTypes)      #type of storage room
        availabilityStatus = random.choice(availabilityStatuses)   #availability status of the storage room
        rentalPricePerDay = round(random.uniform(50.0, 500.0), 2)  #rental price per day in dollars
        
        leaseID = 'NULL'    #default leaseID
        email = 'NULL'      #default email
        
        if availabilityStatus == 'Occupied' or availabilityStatus == 'Reserved':    #assign leaseID and email only if the room is Occupied or Reserved
            leaseID = random.choice(list(lease_dict.keys()))
            email = lease_dict[leaseID]
        else:
            leaseID = 'NULL'
            email = 'NULL'

        writer.writerow([roomID, roomNo, length, width, height, storageType, availabilityStatus, rentalPricePerDay, warehouseID, leaseID, email])


df = pd.read_csv(outputFile)
conn = sqlite3.connect('SRC/StorageRoomManagement.db')
df.to_sql('StorageRoom', conn, if_exists='replace', index=False)
conn.close()
print(f"Generated {numRecords} records in {outputFile}")