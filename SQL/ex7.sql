CREATE VIEW CustomerCityView AS
SELECT 
    c.email,
    c.firstName,
    c.lastName,
    p.city
FROM Customer c
JOIN PostalArea p ON c.postalCode = p.postalCode;

CREATE VIEW LeaseRoomView AS
SELECT 
    la.leaseID,
    la.startDate,
    la.endDate,
    sr.roomID,
    (sr.roomLength * sr.roomWidth) AS floorArea,
    sr.rentalPricePerDay
FROM LeaseAgreement la
JOIN StorageRoom sr ON la.leaseID = sr.leaseID;
