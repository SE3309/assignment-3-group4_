from faker import Faker
import random
import csv
import sqlite3
import pandas as pd

fake = Faker('en_CA')

numRecords = 500
outputFile = 'SRC/storageRoom_data.csv'

storageTypes = ['Cold Storage', 'Dry Storage', 'Hazardous Materials Storage', 'General Storage', 'Bulk Storage']
availabilityStatuses = ['Available', 'Occupied', 'Under Maintenance', 'Reserved']

connect = sqlite3.connect('SRC/StorageRoomManagement.db')
cursor = connect.cursor()
cursor.execute("SELECT warehouseID FROM Warehouse")
warehouseIDs = [row[0] for row in cursor.fetchall()]
connect.close()


# conn = sqlite3.connect('StorageRoomManagement.db')
# cursor = conn.cursor()
# cursor.execute("SELECT leaseID, customerEmail FROM LeaseAgreement")
# lease_data = cursor.fetchall()
# lease_dict = {leaseID: customerEmail for leaseID, customerEmail in lease_data}
# conn.close()




existing_storageRoomIDs = set()

def generate_storageRoomID(index, warehouseID):
    while True:
        storageRoomID = f"SR{warehouseID}{index:04d}"
        if storageRoomID not in existing_storageRoomIDs:
            existing_storageRoomIDs.add(storageRoomID)
            return storageRoomID
        index += 1


with open(outputFile, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['roomID', 'roomNo', 'length', 'width', 'height', 'storageType', 'availabilityStatus', 'rentalPricePerDay', 'warehouseID', 'leaseID', 'customerEmail'])

    for i in range(1, numRecords + 1):
        warehouseID = random.choice(warehouseIDs)
        roomID = generate_storageRoomID(len(existing_storageRoomIDs) + 1, warehouseID)
        roomNo = f"R{random.randint(100, 999)}"
        length = round(random.uniform(5.0, 50.0), 2)
        width = round(random.uniform(5.0, 50.0), 2)
        height = round(random.uniform(3.0, 15.0), 2)
        storageType = random.choice(storageTypes)
        availabilityStatus = random.choice(availabilityStatuses)
        rentalPricePerDay = round(random.uniform(50.0, 500.0), 2)
        
        leaseID = ''
        customerEmail = ''
        
        # if availabilityStatus == 'Occupied' or availabilityStatus == 'Reserved':
        #     leaseID = random.choice(list(lease_dict.keys()))
        #     customerEmail = lease_dict[leaseID]
        # else:
        #     leaseID = ''
        #     customerEmail = ''

        writer.writerow([roomID, roomNo, length, width, height, storageType, availabilityStatus, rentalPricePerDay, warehouseID, leaseID, customerEmail])


df = pd.read_csv(outputFile)
conn = sqlite3.connect('SRC/StorageRoomManagement.db')
df.to_sql('StorageRoom', conn, if_exists='replace', index=False)
conn.close()
print(f"Generated {numRecords} records in {outputFile}")