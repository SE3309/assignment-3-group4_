INSERT INTO Customer SET
firstName = 'Amrit', 
lastName = 'Singh', 
phoneNo = '6471234567', 
dateOfBirth = '1998-05-12' , 
email = 'amrit.singh@gmail.com', 
street= '12B King Street',
postalCode = 'M5V 2T6';

INSERT INTO Customer (firstName, lastName, phoneNo, dateOfBirth, email, street, postalCode)
SELECT
'Jaspreet', 'Kaur', '4169876543', '2000-11-04', 'jaspreet.kaur@gmail.com', '3C Queen Street', postalCode
FROM Customer
WHERE email = 'amrit.singh@gmail.com';

INSERT INTO Customer 
(firstName, lastName, phoneNo, dateOfBirth, email, street, postalCode)
VALUES
('Simran', 'Dhaliwal', '4375557890', '1999-08-30', 'simran.dhaliwal@gmail.com', '22A Front Street', 'L6R 2J3'),
('Raj', 'Patel', '9056671234', '1987-03-18', 'raj.patel@gmail.com', '45 Bay Street', 'N6R 5H3');

