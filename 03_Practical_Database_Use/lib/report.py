import mysql.connector  # type: ignore
from lib.utils import get_connection, print_table, print_error, choose, GoBack

REPORTS = [
    ("Employees, their projects, departments, and roles", "employee_projects"),
    ("Project workload: employees assigned and total hours per project", "project_workload"),
    ("Number of employees per department and their average salary", "department_salary"),
    ("Employee salary levels (High / Medium / Low)", "salary_levels"),
    ("Employees who worked more hours than the company average", "above_average_hours"),
]

QUERIES = {
    "employee_projects": """
        SELECT p.pName, e.FirstName, e.LastName, d.dName, w.Role
        FROM Employee e
        JOIN WorksOn w ON e.eID = w.eID
        JOIN Project p ON w.pID = p.pID
        JOIN Department d ON e.dID = d.dID
        ORDER BY p.pName, e.FirstName, e.LastName
    """,
    "project_workload": """
        SELECT p.pID, p.pName, COUNT(w.eID) NumberOfEmployees, SUM(w.HoursWorked) TotalHours
        FROM Project p
        JOIN WorksOn w ON p.pID = w.pID
        GROUP BY p.pID
        ORDER BY TotalHours DESC
    """,
    "department_salary": """
        SELECT d.dName, COUNT(e.eID) NumberOfEmployees, AVG(e.Salary) AverageSalary
        FROM Department d
        JOIN Employee e ON d.dID = e.dID
        GROUP BY d.dID
        ORDER BY NumberOfEmployees DESC, AverageSalary DESC
    """,
    "salary_levels": """
        SELECT
            eID, FirstName, LastName, Position, Salary,
            CASE
                WHEN Salary >= 90000 THEN 'High'
                WHEN Salary >= 75000 THEN 'Medium'
                ELSE 'Low'
            END SalaryLevel
        FROM Employee
        ORDER BY Salary DESC
    """,
    "above_average_hours": """
        SELECT e.eID, e.FirstName, e.LastName, SUM(w.HoursWorked) TotalHours
        FROM Employee e
        JOIN WorksOn w ON e.eID = w.eID
        GROUP BY e.eID
        HAVING TotalHours > (
            SELECT AVG(EmployeeTotal)
            FROM (
                SELECT SUM(w2.HoursWorked) EmployeeTotal
                FROM Employee e2
                JOIN WorksOn w2 ON e2.eID = w2.eID
                GROUP BY e2.eID
            ) EmployeeHours
        )
        ORDER BY TotalHours DESC
    """,
}

AVERAGE_HOURS_QUERY = """
    SELECT AVG(EmployeeTotal)
    FROM (
        SELECT SUM(w.HoursWorked) EmployeeTotal
        FROM Employee e
        JOIN WorksOn w ON e.eID = w.eID
        GROUP BY e.eID
    ) EmployeeHours
"""


def report(db_config):
    labels = [label for label, _ in REPORTS]
    keys_by_label = dict(REPORTS)

    while True:
        try:
            choice_label = choose(labels, "Available reports:", "Choose a report")
        except GoBack:
            return
        run_report(db_config, keys_by_label[choice_label])


def run_report(db_config, key):
    connection = None
    try:
        connection = get_connection(db_config)
        cursor = connection.cursor()
        try:
            cursor.execute(QUERIES[key])
            rows = cursor.fetchall()
            columns = [d[0] for d in cursor.description]

            average_hours = None
            if key == "above_average_hours":
                cursor.execute(AVERAGE_HOURS_QUERY)
                average_hours = cursor.fetchone()[0]
        finally:
            cursor.close()

        note = None
        if average_hours is not None:
            note = f"Average hours worked: {float(average_hours):.2f}"
        print_table(columns, rows, note=note)
    except mysql.connector.Error as error:
        print_error(error)
    finally:
        if connection and connection.is_connected():
            connection.close()
