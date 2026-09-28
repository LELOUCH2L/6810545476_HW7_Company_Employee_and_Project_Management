import mysql.connector  # type: ignore
from lib.utils import get_connection, print_table, print_error, print_warning, choose, GoBack
from lib.schema import COLUMNS, ask_value, choose_table


def search(db_config):
    while True:
        try:
            table = choose_table()
        except GoBack:
            return
        search_loop(db_config, table)


def search_loop(db_config, table):
    while True:
        try:
            search_once(db_config, table)
        except GoBack:
            return


def choose_field(table):
    return choose(COLUMNS[table], "Available fields:", "Choose a field")


def search_once(db_config, table):
    field = choose_field(table)
    value = ask_value(field, "Enter search value")

    connection = None
    try:
        connection = get_connection(db_config)
        cursor = connection.cursor()
        try:
            cursor.execute(f"SELECT * FROM {table} WHERE {field} LIKE %s", (f"%{value}%",))
            rows = cursor.fetchall()
            columns = [d[0] for d in cursor.description]
        finally:
            cursor.close()

        if not rows:
            print_warning(f"No records found where {field} matches '{value}'.")
        else:
            print_table(columns, rows)
    except mysql.connector.Error as error:
        print_error(error)
    finally:
        if connection and connection.is_connected():
            connection.close()
