CREATE TABLE PostalArea (
    postalCode VARCHAR(8) PRIMARY KEY,
    city VARCHAR(200) NOT NULL
);

CREATE TABLE Warehouse (
    warehouseID CHAR(4) NOT NULL,
    street VARCHAR(300) NOT NULL,
    postalCode VARCHAR(8) NOT NULL,
    PRIMARY KEY (warehouseID),
    FOREIGN KEY (postalCode) REFERENCES PostalArea(postalCode)
);

CREATE TABLE Employee (
    employeeID CHAR(8) NOT NULL,
    firstName VARCHAR(100) NOT NULL,
    lastName VARCHAR(100) NOT NULL,
    phoneNo VARCHAR(25) NOT NULL,
    email VARCHAR(255) NOT NULL,
    empRole VARCHAR(100),
    warehouseID CHAR(4) NOT NULL,
    PRIMARY KEY (employeeID),
    FOREIGN KEY (warehouseID) REFERENCES Warehouse(warehouseID)
);

CREATE TABLE Customer (
    email VARCHAR(255) NOT NULL,
    firstName VARCHAR(100) NOT NULL,
    lastName VARCHAR(100) NOT NULL,
    phoneNo VARCHAR(30) NOT NULL,
    dateOfBirth DATE NOT NULL,
    street VARCHAR(300) NOT NULL,
    postalCode VARCHAR(8) NOT NULL,
    PRIMARY KEY (email),
    FOREIGN KEY (postalCode) REFERENCES PostalArea(postalCode)
);

CREATE TABLE Transactions (
    transactionID CHAR(7) NOT NULL,
    amount DECIMAL(19,2) NOT NULL,
    paymentType VARCHAR(100) NOT NULL,
    paymentDetails VARCHAR(100) NOT NULL,
    transactionDate DATE NOT NULL,
    transactionStatus VARCHAR(20) NOT NULL,
    email VARCHAR(255) NOT NULL,
    PRIMARY KEY (transactionID),
    FOREIGN KEY (email) REFERENCES Customer(email)
);

CREATE TABLE Discount (
    discountID CHAR(4) PRIMARY KEY,
    discountCode VARCHAR(100) NOT NULL,
    percentage SMALLINT NOT NULL
);

CREATE TABLE LeaseAgreement (
    leaseID CHAR(6) NOT NULL,
    startDate DATE NOT NULL,
    endDate DATE NOT NULL,
    leaseConditions VARCHAR(200),
    transactionID CHAR(7) NOT NULL,
    email VARCHAR(255) NOT NULL,
    discountID CHAR(4),
    PRIMARY KEY (leaseID),
    FOREIGN KEY (transactionID) REFERENCES Transactions(transactionID),
    FOREIGN KEY (email) REFERENCES Customer(email),
    FOREIGN KEY (discountID) REFERENCES Discount(discountID)
);
CREATE TABLE StorageRoom (
    roomID CHAR(10) NOT NULL,
    roomNo CHAR(4) NOT NULL,
    roomLength DECIMAL(10,2) NOT NULL,
    roomWidth DECIMAL(10,2) NOT NULL,
    roomHeight DECIMAL(10,2) NOT NULL,
    storageType VARCHAR(100) NOT NULL,
    availabilityStatus VARCHAR(100) NOT NULL,
    rentalPricePerDay DECIMAL(19,2) NOT NULL,
    warehouseID CHAR(4) NOT NULL,
    email VARCHAR(255) NOT NULL,
    leaseID CHAR(6) NOT NULL,
    PRIMARY KEY (roomID),
    FOREIGN KEY (warehouseID) REFERENCES Warehouse(warehouseID),
    FOREIGN KEY (email) REFERENCES Customer(email),
    FOREIGN KEY (leaseID) REFERENCES LeaseAgreement(leaseID)
);
