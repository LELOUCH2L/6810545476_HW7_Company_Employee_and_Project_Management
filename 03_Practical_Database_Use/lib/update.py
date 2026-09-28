import mysql.connector  # type: ignore
from lib.utils import get_connection, print_info, print_warning, print_success, print_error, choose, pause, GoBack
from lib.schema import PK, EDITABLE_FIELDS, FOREIGN_KEYS, ask_value, choose_table, show_table, show_referenced


def update(db_config):
    while True:
        try:
            table = choose_table()
        except GoBack:
            return
        update_loop(db_config, table)


def update_loop(db_config, table):
    while True:
        try:
            update_once(db_config, table)
        except GoBack:
            return
        pause()


def choose_editable_field(table):
    return choose(EDITABLE_FIELDS[table], "Editable fields:", "Choose a field to update")


def update_once(db_config, table):
    connection = None
    try:
        connection = get_connection(db_config)
        cursor = connection.cursor()
        try:
            show_table(cursor, table, f"Update {table}")

            pk_fields = PK[table]
            pk_values = [ask_value(key, f"Enter {key}") for key in pk_fields]

            where = " AND ".join(f"{key} = %s" for key in pk_fields)
            cursor.execute(f"SELECT * FROM {table} WHERE {where}", pk_values)
            rows = cursor.fetchall()
            columns = [d[0] for d in cursor.description]

            if not rows:
                print_warning("No matching record found.")
                return

            record = dict(zip(columns, rows[0]))

            field = choose_editable_field(table)
            print_info(f"Current value: {record[field]}")

            if field in FOREIGN_KEYS.get(table, {}):
                show_referenced(cursor, FOREIGN_KEYS[table][field])

            new_value = ask_value(field, f"Enter new value for {field}")

            cursor.execute(f"UPDATE {table} SET {field} = %s WHERE {where}", [new_value] + pk_values)
            connection.commit()
            print_success("Record updated successfully.")
        finally:
            cursor.close()
    except mysql.connector.Error as error:
        print_error(error)
    finally:
        if connection and connection.is_connected():
            connection.close()
