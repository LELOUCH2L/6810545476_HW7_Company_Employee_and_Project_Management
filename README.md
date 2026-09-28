# HW7 - Company Employee and Project Management System

**Option:** C - Simple Database Application  
**Database:** MySQL  
**Programming Language:** Python

## 1. Project Overview

This project is a Company Employee and Project Management System.

The system manages departments, employees, projects, and employee-project assignments.

The database contains four main tables:

- `Department`
- `Employee`
- `Project`
- `WorksOn`

## 2. Project Structure

```text
6810545476_HW7_Company_Employee_and_Project_Management/
├── 01_Report/
│   └── 6810545476_HW7_Report.pdf
├── 02_Database/
│   └── 6810545476_HW7.sql
├── 03_Practical_Database_Use/
│   ├── lib/
│   │   ├── config.py
│   │   ├── delete.py
│   │   ├── display.py
│   │   ├── insert.py
│   │   ├── report.py
│   │   ├── reset.py
│   │   ├── schema.py
│   │   ├── search.py
│   │   ├── update.py
│   │   └── utils.py
│   ├── main.py
│   └── requirements.txt
├── 04_Screenshots/
│   ├── database_implementation1.png
│   ├── database_implementation2.png
│   ├── practical_database_use1.png
│   ├── practical_database_use2.png
│   ├── validation_and_testing_constraint.png
│   ├── validation_and_testing_insert.png
│   ├── validation_and_testing_report.png
│   └── validation_and_testing_update.png
├── .gitignore
└── README.md
```

## 3. Database Schema

### Department

- `dID` - Primary key
- `dName` - Unique department name

### Employee

- `eID` - Primary key
- `FirstName`
- `LastName`
- `Email` - Unique email
- `Position`
- `Salary`
- `dID` - Foreign key referencing `Department`

### Project

- `pID` - Primary key
- `pName` - Unique project name
- `StartDate`
- `dID` - Foreign key referencing `Department`

### WorksOn

- `eID` - Foreign key referencing `Employee`
- `pID` - Foreign key referencing `Project`
- `Role`
- `HoursWorked`
- Composite primary key: `(eID, pID)`

Database name:

```text
hw7_6810545476
```

## 4. Requirements

- **Python:** 3.13
- **Database:** MySQL
- **Python Package:** `mysql-connector-python==26.7.0`
- A running MySQL server is required.

The required Python package and its version are specified in:

```text
03_Practical_Database_Use/requirements.txt
```

## 5. How to Run

1. Start the MySQL server.
2. Clone the repository.
   
   **Windows**

   Open **Command Prompt**, **PowerShell**, or **Git Bash**:
   ```bash
   git clone https://github.com/LELOUCH2L/6810545476_HW7_Company_Employee_and_Project_Management.git
   cd 6810545476_HW7_Company_Employee_and_Project_Management/03_Practical_Database_Use
   ```

   **macOS / Linux**

   Open **Terminal**:
   ```sh
   git clone https://github.com/LELOUCH2L/6810545476_HW7_Company_Employee_and_Project_Management.git
   cd 6810545476_HW7_Company_Employee_and_Project_Management/03_Practical_Database_Use
   ```

3. Create a virtual environment.  

   **Windows**
   ```bash
   python -m venv .venv
   ```

   **macOS / Linux**
   ```sh
   python3 -m venv .venv
   ```

4. Activate the virtual environment.

   **Windows CMD**
   ```cmd
   .venv\Scripts\activate
   ```

   **Windows PowerShell**
   ```powershell
   .venv\Scripts\Activate.ps1
   ```

   **macOS / Linux**
   ```sh
   source .venv/bin/activate
   ```

5. Install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```

6. Run the application.

   **Windows**
   ```bash
   python main.py
   ```

   **macOS / Linux**
   ```sh
   python3 main.py
   ```

7. Enter the MySQL host, username, and password.

The application checks the database connection and initializes the database and tables from the SQL file when the database has not been initialized.

## 6. Application Commands

| Command | Description |
|---|---|
| `insert` | Insert a record into a selected table |
| `display` | Display records from a selected table |
| `search` | Search records by a selected field using partial matching |
| `report` | Generate predefined SQL reports |
| `update` | Update an editable field of an existing record |
| `delete` | Delete a record after confirmation |
| `reset` | Reset a table or the entire database, with or without sample data |
| `clear` | Clear the terminal screen |
| `quit` | Exit the application |

## 7. Reports

The application provides five reports:

1. Employees, their projects, departments, and roles
2. Project workload, including assigned employees and total hours
3. Number of employees and average salary by department
4. Employee salary levels: High, Medium, or Low
5. Employees whose total project hours are above the company average

These reports use SQL joins, grouping, aggregate functions, `CASE`, and a subquery.

## 8. Database Setup

The SQL script is located at:

```text
02_Database/6810545476_HW7.sql
```

The script creates the `hw7_6810545476` database and the four tables, then inserts sample data.

Tables:

- `Department`
- `Employee`
- `Project`
- `WorksOn`

The sample data contains:

- 5 departments
- 5 employees
- 5 projects
- 10 employee-project assignments

The application also uses this SQL file when resetting the entire database.
