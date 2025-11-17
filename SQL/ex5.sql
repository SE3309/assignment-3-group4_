/* Finding all managers that work in London warehouses using
JOIN */
SELECT
  e.employeeID, e.firstName, e.lastName, e.email, e.branch, e.warehouseID
FROM Employee AS e
JOIN Warehouse AS w
  ON e.warehouseID = w.warehouseID
JOIN City AS c
  ON w.postalCode = c.postalCode
WHERE e.role = 'Manager'
  AND c.city = 'London'
ORDER BY e.lastName, e.firstName;



/* Showing all rooms that cost above the average price for 
their own storage type using AVG */
SELECT r.roomID, r.roomNo, r.storageType, r.rentalPrice
FROM Room AS r
WHERE r.rentalPrice >
      (SELECT AVG(r2.rentalPrice)
       FROM Room AS r2
       WHERE r2.storageType = r.storageType)
ORDER BY r.storageType, r.rentalPrice DESC;



/* Shows all warehouses that have at least one available 
cold storage room using EXISTS semi-join */
SELECT
  w.warehouseID, w.street, c.city
FROM Warehouse AS w
JOIN City AS c
  ON w.postalCode = c.postalCode
WHERE EXISTS (
  SELECT 1
  FROM Room AS r
  WHERE r.warehouseID = w.warehouseID
    AND r.storageType = 'Cold Storage'
    AND r.availabilityStatus = 'Available'
)
ORDER BY c.city, w.warehouseID;