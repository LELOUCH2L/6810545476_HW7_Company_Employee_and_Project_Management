import mysql.connector  # type: ignore
from lib.utils import get_connection, print_success, print_error, tight, pause, GoBack
from lib.schema import COLUMNS, FOREIGN_KEYS, ask_value, choose_table, show_table, show_referenced


def insert(db_config):
    with tight():
        while True:
            try:
                table = choose_table()
            except GoBack:
                return
            insert_loop(db_config, table)


def insert_loop(db_config, table):
    while True:
        try:
            insert_once(db_config, table)
        except GoBack:
            return
        pause()


def insert_once(db_config, table):
    connection = None
    try:
        connection = get_connection(db_config)
        cursor = connection.cursor()
        try:
            show_table(cursor, table, f"Insert into {table}")

            values = []
            for field in COLUMNS[table]:
                if field in FOREIGN_KEYS.get(table, {}):
                    show_referenced(cursor, FOREIGN_KEYS[table][field])
                values.append(ask_value(field, f"Enter {field}"))

            columns_sql = ", ".join(COLUMNS[table])
            placeholders = ", ".join(["%s"] * len(values))
            cursor.execute(f"INSERT INTO {table} ({columns_sql}) VALUES ({placeholders})", values)
            connection.commit()
            print_success("Record inserted successfully.")
        finally:
            cursor.close()
    except mysql.connector.Error as error:
        print_error(error)
    finally:
        if connection and connection.is_connected():
            connection.close()
