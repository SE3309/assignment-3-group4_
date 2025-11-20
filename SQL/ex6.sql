UPDATE StorageRoom
SET availabilityStatus = 'Available'
WHERE leaseID IN (
    SELECT leaseID
    FROM LeaseAgreement
    WHERE DATE(endDate) < DATE(NOW())
);



-- -----------------------------------

DELETE FROM Transactions t
WHERE t.transactionStatus = 'Cancelled'
  AND t.amount < 200
  AND t.transactionDate < DATE_SUB(CURDATE(), INTERVAL 18 MONTH)
  AND EXISTS (
        SELECT 1
        FROM Customer c
        WHERE c.email = t.email
          -- AND c.city = 'Toronto'
          AND c.dateOfBirth < DATE('1990-01-01')
  );

-- ----------------------------------

UPDATE StorageRoom
SET rentalPricePerDay = rentalPricePerDay * 1.15
WHERE storageType = 'Bulk Storage';


 
