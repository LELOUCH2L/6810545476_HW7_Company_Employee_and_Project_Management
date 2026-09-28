-- HW7: Option C
-- Domain: Company Employee and Project Management

DROP DATABASE IF EXISTS hw7_6810545476;
CREATE DATABASE hw7_6810545476;
USE hw7_6810545476;

-- Create Tables

CREATE TABLE Department (
    dID CHAR(4) PRIMARY KEY,
    dName VARCHAR(100) NOT NULL UNIQUE
);

CREATE TABLE Employee (
    eID CHAR(4) PRIMARY KEY,
    FirstName VARCHAR(100) NOT NULL,
    LastName VARCHAR(100) NOT NULL,
    Email VARCHAR(100) NOT NULL UNIQUE,
    Position VARCHAR(100) NOT NULL,
    Salary DECIMAL(9,2) NOT NULL CHECK (Salary >= 0),
    dID CHAR(4) NOT NULL,

    FOREIGN KEY (dID) REFERENCES Department(dID)
        ON UPDATE CASCADE
);

CREATE TABLE Project (
    pID CHAR(4) PRIMARY KEY,
    pName VARCHAR(100) NOT NULL UNIQUE,
    StartDate DATE NOT NULL,
    dID CHAR(4) NOT NULL,

    FOREIGN KEY (dID) REFERENCES Department(dID)
        ON UPDATE CASCADE
);

CREATE TABLE WorksOn (
    eID CHAR(4),
    pID CHAR(4),
    Role VARCHAR(100) NOT NULL,
    HoursWorked INT NOT NULL DEFAULT 0 CHECK (HoursWorked >= 0),

    PRIMARY KEY (eID, pID),

    FOREIGN KEY (eID) REFERENCES Employee(eID)
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    FOREIGN KEY (pID) REFERENCES Project(pID)
        ON UPDATE CASCADE
        ON DELETE CASCADE
);

-- Sample Data

INSERT INTO Department
(dID, dName) VALUES
('D001', 'Engineering'),
('D002', 'Human Resources'),
('D003', 'Finance'),
('D004', 'Marketing'),
('D005', 'Information Technology');

INSERT INTO Employee
(eID, FirstName, LastName, Email, Position, Salary, dID) VALUES
('E001', 'Alice', 'Johnson', 'alice.johnson@company.com', 'Software Engineer', 85000.00, 'D001'),
('E002', 'Brian', 'Smith', 'brian.smith@company.com', 'HR Specialist', 68000.00, 'D002'),
('E003', 'Clara', 'Williams', 'clara.williams@company.com', 'Finance Manager', 95000.00, 'D003'),
('E004', 'Daniel', 'Brown', 'daniel.brown@company.com', 'Marketing Specialist', 70000.00, 'D004'),
('E005', 'Emma', 'Davis', 'emma.davis@company.com', 'Systems Engineer', 88000.00, 'D005');

INSERT INTO Project
(pID, pName, StartDate, dID) VALUES
('P001', 'Mobile Application Development', '2026-01-15', 'D001'),
('P002', 'Employee Portal', '2026-02-01', 'D002'),
('P003', 'Annual Budget Planning', '2026-01-20', 'D003'),
('P004', 'Website Redesign', '2026-03-10', 'D004'),
('P005', 'Cloud Migration', '2026-02-15', 'D005');

INSERT INTO WorksOn
(eID, pID, Role, HoursWorked) VALUES
('E001', 'P001', 'Lead Developer', 150),
('E001', 'P005', 'Backend Developer', 60),
('E002', 'P002', 'Project Coordinator', 90),
('E002', 'P004', 'Content Reviewer', 40),
('E003', 'P003', 'Budget Owner', 80),
('E003', 'P002', 'Finance Advisor', 30),
('E004', 'P004', 'UI Specialist', 100),
('E004', 'P001', 'Marketing Liaison', 35),
('E005', 'P005', 'Project Lead', 120),
('E005', 'P001', 'Systems Engineer', 45);
