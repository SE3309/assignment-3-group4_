/* Showing top 50 longest running lease in the system */
SELECT la.leaseID, la.startDate, la.endDate, la.transactionID, la.email, t.amount, 
DATEDIFF(la.endDate, la.startDate) AS leaseDuration
FROM LeaseAgreement la
LEFT JOIN Transactions AS t
	ON la.transactionID = t.transactionID
ORDER BY 
	leaseDuration DESC
LIMIT 50;


/* Showing all rooms that cost above the average price for 
their own storage type using AVG */
SELECT r.roomID, r.roomNo, r.storageType, r.rentalPricePerDay
FROM StorageRoom AS r
WHERE r.rentalPricePerDay >
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


/* total revenue for each warehouse */
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
    c.email,
    c.firstName,
    c.lastName,
    COUNT(sr.roomID) AS roomsRented
FROM Customer c
LEFT JOIN LeaseAgreement la
    ON la.email = c.email    
LEFT JOIN StorageRoom sr
    ON sr.leaseID = la.leaseID
GROUP BY
    c.email,
    c.firstName,
    c.lastName
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


/*Find all storages that will be available in the next 2 weeks and have a rental price less than 300*/
SELECT sr.roomID, sr.warehouseID, sr.storageType, sr.email, sr.rentalPricePerDay, DATEDIFF(la.endDate, NOW()) AS daysRemaining
FROM StorageRoom sr
LEFT JOIN LeaseAgreement la
    ON sr.leaseID = la.leaseID
WHERE
    (
        la.endDate IS NOT NULL
        AND DATE(la.endDate) <= DATE_ADD(NOW(), INTERVAL 28 DAY)
    )
    AND
	(
 		DATEDIFF(la.endDate, NOW()) > 0
	);