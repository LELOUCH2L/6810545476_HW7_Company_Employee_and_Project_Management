import mysql.connector  # type: ignore
from pathlib import Path
from lib.config import DATABASE_NAME, SQL_FILE
from lib.utils import (
    get_connection, print_success, print_error, print_caution, choose, confirm,
    pause, read_sql_statements, GoBack
)
from lib.schema import choose_table


def reset(db_config):
    while True:
        try:
            mode = choose(["Table", "Database"], "Available options:", "Choose an option")
        except GoBack:
            return

        if mode == "Table":
            reset_table(db_config)
        else:
            reset_database(db_config)


def reset_table(db_config):
    try:
        table = choose_table()
        reset_table_once(db_config, table)
        pause()
    except GoBack:
        return


def reset_table_once(db_config, table):
    print_caution(f"This will delete all records from {table}.")

    if not confirm("Are you sure?"):
        print_success("Reset cancelled.")
        return

    connection = None
    try:
        connection = get_connection(db_config)
        cursor = connection.cursor()
        try:
            cursor.execute(f"DELETE FROM {table}")
            connection.commit()
            print_success(f"All records deleted from {table}.")
        finally:
            cursor.close()
    except mysql.connector.Error as error:
        print_error(error)
    finally:
        if connection and connection.is_connected():
            connection.close()


def reset_database(db_config):
    try:
        choice_label = choose(
            ["Default (with sample data)", "Empty (no sample data)"],
            "Available options:", "Choose an option"
        )
        choice = "default" if choice_label == "Default (with sample data)" else "empty"
        reset_database_once(db_config, choice)
        pause()
    except GoBack:
        return


def reset_database_once(db_config, choice):
    label = "with sample data" if choice == "default" else "with no sample data"
    print_caution(f"This will reset the entire database {label}.")

    if not confirm("Are you sure?"):
        print_success("Reset cancelled.")
        return

    sql_path = Path(__file__).resolve().parents[2] / "02_Database" / SQL_FILE
    connection = None
    try:
        connection = mysql.connector.connect(
            host=db_config["host"], user=db_config["user"], password=db_config["password"]
        )
        cursor = connection.cursor()
        try:
            cursor.execute(f"DROP DATABASE IF EXISTS `{DATABASE_NAME}`")

            for statement in read_sql_statements(sql_path):
                if choice == "empty" and statement.upper().startswith("INSERT INTO"):
                    continue
                cursor.execute(statement)

            connection.commit()
            print_success("Database reset successfully.")
        finally:
            cursor.close()
    except (mysql.connector.Error, OSError) as error:
        if connection:
            connection.rollback()
        print_error(error)
    finally:
        if connection and connection.is_connected():
            connection.close()
