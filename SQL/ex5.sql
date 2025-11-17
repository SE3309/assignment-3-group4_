/* Finding all managers that work in London warehouses using
JOIN */
SELECT
  e.employeeID, e.firstName, e.lastName, e.email, e.warehouseID, e.empRole
FROM Employee AS e
JOIN Warehouse AS w
  ON e.warehouseID = w.warehouseID
JOIN City AS c
  ON w.postalCode = c.postalCode
WHERE e.empRole = 'Manager'
  AND c.city = 'London'
ORDER BY e.lastName, e.firstName;



/* Showing all rooms that cost above the average price for 
their own storage type using AVG */
SELECT r.roomID, r.roomNo, r.storageType, r.rentalPricePerDay
FROM StorageRoom AS r
WHERE r.rentalPrice >
      (SELECT AVG(r2.rentalPricePerDay)
       FROM StorageRoom AS r2
       WHERE r2.storageType = r.storageType)
ORDER BY r.storageType, r.rentalPricePerDay DESC;



/* Shows all warehouses that have at least one available 
cold storage room using EXISTS semi-join */
SELECT
  w.warehouseID, w.street, p.postalcode
FROM Warehouse AS w
JOIN PostalArea AS p
  ON w.postalCode = p.postalCode
WHERE EXISTS (
  SELECT 1
  FROM StorageRoom AS r
  WHERE r.warehouseID = w.warehouseID
    AND r.storageType = 'Cold Storage'
    AND r.availabilityStatus = 'Available'
)
ORDER BY p.postalCode, w.warehouseID;

/* total revenue for each warehousem */
SELECT 
    w.warehouseID,
    COALESCE(SUM(t.amount), 0) AS totalRevenue
FROM Warehouse w
LEFT JOIN StorageRoom sr 
    ON sr.warehouseID = w.warehouseID
LEFT JOIN LeaseAgreement la 
    ON la.leaseID = sr.leaseID
LEFT JOIN Transactions t 
    ON t.transactionID = la.transactionID
GROUP BY w.warehouseID
ORDER BY totalRevenue DESC;

/*Find customers who rented more than one room */
SELECT
    c.customerID,
    c.fName,
    c.lName,
    COUNT(sr.roomID) AS roomsRented
FROM Customer c
LEFT JOIN LeaseAgreement la
    ON la.customerID = c.customerID     
LEFT JOIN StorageRoom sr
    ON sr.leaseID = la.leaseID
GROUP BY
    c.customerID,
    c.fName,
    c.lName
HAVING
    COUNT(sr.roomID) > 1
ORDER BY roomsRented DESC;

/* Calculate the occupancy rate for each warehouse */
SELECT w.warehouseID AS warehouse,
COUNT(s.roomID) AS total_rooms,
SUM(s.availabilityStatus = 'Occupied') AS occupied_rooms,
ROUND(100.0 * SUM(s.availabilityStatus = 'Occupied') / NULLIF(COUNT(s.roomID), 0), 2) AS occupancy_rate
FROM Warehouse w
LEFT JOIN StorageRoom s ON w.warehouseID = s.warehouseID
GROUP BY w.warehouseID
ORDER BY occupancy_rate DESC;