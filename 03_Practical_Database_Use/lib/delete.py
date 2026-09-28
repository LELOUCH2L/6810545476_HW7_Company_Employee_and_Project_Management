import mysql.connector  # type: ignore
from lib.utils import get_connection, print_warning, print_success, print_error, print_caution, confirm, pause, GoBack
from lib.schema import PK, ask_value, choose_table, show_table


def delete(db_config):
    while True:
        try:
            table = choose_table()
        except GoBack:
            return
        delete_loop(db_config, table)


def delete_loop(db_config, table):
    while True:
        try:
            delete_once(db_config, table)
        except GoBack:
            return
        pause()


def delete_once(db_config, table):
    connection = None
    try:
        connection = get_connection(db_config)
        cursor = connection.cursor()
        try:
            show_table(cursor, table, f"Delete from {table}")

            pk_fields = PK[table]
            pk_values = [ask_value(key, f"Enter {key}") for key in pk_fields]

            where = " AND ".join(f"{key} = %s" for key in pk_fields)
            cursor.execute(f"SELECT * FROM {table} WHERE {where}", pk_values)
            rows = cursor.fetchall()

            if not rows:
                print_warning("No matching record found.")
                return

            print_caution(
                f"This will delete the following record from {table}: "
                f"({', '.join(str(value) for value in rows[0])})"
            )

            if not confirm("Are you sure?"):
                print_success("Deletion cancelled.")
                return

            cursor.execute(f"DELETE FROM {table} WHERE {where}", pk_values)
            connection.commit()
            print_success("Record deleted successfully.")
        finally:
            cursor.close()
    except mysql.connector.Error as error:
        print_error(error)
    finally:
        if connection and connection.is_connected():
            connection.close()
