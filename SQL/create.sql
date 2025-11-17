CREATE TABLE PostalArea (
	postalCode VARCHAR(8) PRIMARY KEY,
    city VARCHAR(200) NOT NULL
);
CREATE TABLE Warehouse (
	warehouseID INT PRIMARY KEY AUTO_INCREMENT,
    street VARCHAR(300) NOT NULL,
    warehousePostalCode VARCHAR(8),
    CONSTRAINT warehousePostalCode FOREIGN KEY (warehousePostalCode)
    REFERENCES PostalArea (postalCode) 
);
CREATE TABLE Employee (
	employeeID INT PRIMARY KEY AUTO_INCREMENT,
	fName VARCHAR(100) NOT NULL,
    lName VARCHAR(100) NOT NULL,
    phoneNO VARCHAR(25) NOT NULL,
    email VARCHAR(320) NOT NULL,
    empRole VARCHAR(100),
    empWarehouseID INT,
    CONSTRAINT empWarehouseID FOREIGN KEY (empWarehouseID)
    REFERENCES Warehouse (warehouseID)
);
CREATE TABLE Customer (
	emailAddress VARCHAR(255) PRIMARY KEY,
    fName VARCHAR(100) NOT NULL,
    lName VARCHAR(100) NOT NULL,
    phoneNo VARCHAR(30) NOT NULL,
	DateOfBirth DATE NOT NULL,
	unit VARCHAR(20),
    street VARCHAR(300) NOT NULL,
    customerPostalCode VARCHAR(8),
    CONSTRAINT customerPostalCode FOREIGN KEY (customerPostalCode)
    REFERENCES PostalArea (postalCode)
);
CREATE TABLE Transactions (
	transactionID INT PRIMARY KEY AUTO_INCREMENT,
    amount DECIMAL(19, 2) NOT NULL,
    paymentType VARCHAR(100) NOT NULL,
    transactionDate DATE NOT NULL,
    transactionStatus VARCHAR(20),
	transactionEmailAddress VARCHAR(255),
    CONSTRAINT transactionEmailAddress FOREIGN KEY (transactionEmailAddress)
    REFERENCES Customer (emailAddress)
);
CREATE TABLE Discount (
	discountID INT PRIMARY KEY AUTO_INCREMENT,
    discountCode VARCHAR(100) NOT NULL,
    percentage DECIMAL(5, 4) NOT NULL
);
CREATE TABLE LeaseAgreement (
	leaseID INT PRIMARY KEY AUTO_INCREMENT,
    startDATE DATE NOT NULL,
    endDATE DATE NOT NULL,
    leaseConditions VARCHAR(200),
    transactionID INT,
    leaseEmailAddress VARCHAR(255),
    discountID INT,
    CONSTRAINT transactionID FOREIGN KEY (transactionID)
    REFERENCES Transactions (transactionID),
    CONSTRAINT leaseEmailAddress FOREIGN KEY (leaseEmailAddress)
    REFERENCES Customer (emailAddress),
    CONSTRAINT discountID FOREIGN KEY (discountID)
    REFERENCES Discount (discountID)
);
CREATE TABLE StorageRoom (
	roomID INT PRIMARY KEY AUTO_INCREMENT,
    roomNo SMALLINT NOT NULL,
    roomLength DECIMAL(10, 2) NOT NULL,
    roomWidth DECIMAL(10, 2) NOT NULL,
    roomHeight DECIMAL(10, 2) NOT NULL,
    storageType VARCHAR(100),
    availabilityStatus VARCHAR(100) NOT NULL,
    rentalPricePerDay DECIMAL(19, 2) NOT NULL,
    roomWarehouseID INT,
    roomEmailAddress VARCHAR(255),
    leaseID INT,
	CONSTRAINT roomWarehouseID FOREIGN KEY (roomWarehouseID)
    REFERENCES Warehouse (warehouseID),
    CONSTRAINT roomEmailAddress FOREIGN KEY (roomEmailAddress)
    REFERENCES Customer (emailAddress),
	CONSTRAINT leaseID FOREIGN KEY (leaseID)
    REFERENCES LeaseAgreement (leaseID)
);


    