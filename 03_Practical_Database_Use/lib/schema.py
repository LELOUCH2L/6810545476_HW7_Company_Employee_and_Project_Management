from lib.utils import ask, choose, print_table

TABLES = ["Department", "Employee", "Project", "WorksOn"]

PK = {
    "Department": ["dID"],
    "Employee": ["eID"],
    "Project": ["pID"],
    "WorksOn": ["eID", "pID"],
}

COLUMNS = {
    "Department": ["dID", "dName"],
    "Employee": ["eID", "FirstName", "LastName", "Email", "Position", "Salary", "dID"],
    "Project": ["pID", "pName", "StartDate", "dID"],
    "WorksOn": ["eID", "pID", "Role", "HoursWorked"],
}

EDITABLE_FIELDS = {
    "Department": ["dName"],
    "Employee": ["FirstName", "LastName", "Email", "Position", "Salary", "dID"],
    "Project": ["pName", "StartDate", "dID"],
    "WorksOn": ["Role", "HoursWorked"],
}

FOREIGN_KEYS = {
    "Employee": {"dID": {"table": "Department", "show": ["dID", "dName"]}},
    "Project": {"dID": {"table": "Department", "show": ["dID", "dName"]}},
    "WorksOn": {
        "eID": {"table": "Employee", "show": ["eID", "FirstName", "LastName"]},
        "pID": {"table": "Project", "show": ["pID", "pName"]},
    },
}

KEY_FIELDS = {"dID", "eID", "pID"}


def ask_value(field, prompt):
    return ask(prompt, key=field in KEY_FIELDS)


def choose_table():
    return choose(TABLES, "Available tables:", "Choose a table")


def select_all(table):
    return f"SELECT * FROM {table} ORDER BY {', '.join(PK[table])}"


def show_table(cursor, table, title):
    cursor.execute(select_all(table))
    rows = cursor.fetchall()
    columns = [d[0] for d in cursor.description]
    print_table(columns, rows, title=title)


def show_referenced(cursor, fk):
    cursor.execute(f"SELECT {', '.join(fk['show'])} FROM {fk['table']} ORDER BY {', '.join(PK[fk['table']])}")
    print_table(fk["show"], cursor.fetchall(), title=f"Available {fk['table']} records:")
