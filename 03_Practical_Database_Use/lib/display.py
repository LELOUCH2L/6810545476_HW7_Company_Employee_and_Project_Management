import mysql.connector  # type: ignore
from lib.utils import get_connection, print_table, print_error, GoBack
from lib.schema import choose_table, select_all


def display(db_config):
    while True:
        try:
            table = choose_table()
        except GoBack:
            return
        display_once(db_config, table)


def display_once(db_config, table):
    connection = None
    try:
        connection = get_connection(db_config)
        cursor = connection.cursor()
        try:
            cursor.execute(select_all(table))
            rows = cursor.fetchall()
            columns = [d[0] for d in cursor.description]
        finally:
            cursor.close()

        print_table(columns, rows)
    except mysql.connector.Error as error:
        print_error(error)
    finally:
        if connection and connection.is_connected():
            connection.close()
