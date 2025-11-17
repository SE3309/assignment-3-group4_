CREATE TABLE PostalArea (
    postalCode VARCHAR(8) PRIMARY KEY,
    city VARCHAR(200) NOT NULL
);

CREATE TABLE Warehouse (
    warehouseID INT NOT NULL AUTO_INCREMENT,
    street VARCHAR(300) NOT NULL,
    postalCode VARCHAR(8) NOT NULL,
    PRIMARY KEY (warehouseID),
    FOREIGN KEY (postalCode) REFERENCES PostalArea(postalCode)
);

CREATE TABLE Employee (
    employeeID INT NOT NULL AUTO_INCREMENT,
    fName VARCHAR(100) NOT NULL,
    lName VARCHAR(100) NOT NULL,
    phoneNO VARCHAR(25) NOT NULL,
    email VARCHAR(320) NOT NULL,
    empRole VARCHAR(100),
    warehouseID INT NOT NULL,
    PRIMARY KEY (employeeID),
    FOREIGN KEY (warehouseID) REFERENCES Warehouse(warehouseID)
);

CREATE TABLE Customer (
    emailAddress VARCHAR(255) NOT NULL,
    fName VARCHAR(100) NOT NULL,
    lName VARCHAR(100) NOT NULL,
    phoneNo VARCHAR(30) NOT NULL,
    DateOfBirth DATE NOT NULL,
    unit VARCHAR(20),
    street VARCHAR(300) NOT NULL,
    postalCode VARCHAR(8) NOT NULL,
    PRIMARY KEY (emailAddress),
    FOREIGN KEY (postalCode) REFERENCES PostalArea(postalCode)
);

CREATE TABLE Transactions (
    transactionID INT NOT NULL AUTO_INCREMENT,
    amount DECIMAL(19,2) NOT NULL,
    paymentType VARCHAR(100) NOT NULL,
    transactionDate DATE NOT NULL,
    transactionStatus VARCHAR(20),
    emailAddress VARCHAR(255) NOT NULL,
    PRIMARY KEY (transactionID),
    FOREIGN KEY (emailAddress) REFERENCES Customer(emailAddress)
);

CREATE TABLE Discount (
    discountID INT PRIMARY KEY AUTO_INCREMENT,
    discountCode VARCHAR(100) NOT NULL,
    percentage DECIMAL(5,4) NOT NULL
);

CREATE TABLE LeaseAgreement (
    leaseID INT NOT NULL AUTO_INCREMENT,
    startDATE DATE NOT NULL,
    endDATE DATE NOT NULL,
    leaseConditions VARCHAR(200),
    transactionID INT NOT NULL,
    emailAddress VARCHAR(255) NOT NULL,
    discountID INT,
    PRIMARY KEY (leaseID),
    FOREIGN KEY (transactionID) REFERENCES Transactions(transactionID),
    FOREIGN KEY (emailAddress) REFERENCES Customer(emailAddress),
    FOREIGN KEY (discountID) REFERENCES Discount(discountID)
);
CREATE TABLE StorageRoom (
    roomID INT NOT NULL AUTO_INCREMENT,
    roomNo SMALLINT NOT NULL,
    roomLength DECIMAL(10,2) NOT NULL,
    roomWidth DECIMAL(10,2) NOT NULL,
    roomHeight DECIMAL(10,2) NOT NULL,
    storageType VARCHAR(100),
    availabilityStatus VARCHAR(100) NOT NULL,
    rentalPricePerDay DECIMAL(19,2) NOT NULL,
    warehouseID INT NOT NULL,
    emailAddress VARCHAR(255),
    leaseID INT,
    PRIMARY KEY (roomID),
    FOREIGN KEY (warehouseID) REFERENCES Warehouse(warehouseID),
    FOREIGN KEY (emailAddress) REFERENCES Customer(emailAddress),
    FOREIGN KEY (leaseID) REFERENCES LeaseAgreement(leaseID)
);
