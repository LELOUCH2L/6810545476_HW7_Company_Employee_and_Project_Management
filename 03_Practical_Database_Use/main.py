import os
import sys
import time
from pathlib import Path

import mysql.connector  # type: ignore
from lib.config import DATABASE_NAME, SQL_FILE
from lib.schema import TABLES
from lib.utils import enable_ansi, print_error, print_success, print_warning, read_sql_statements, reset_gap, BAR, BLUE, RESET

if os.name == "nt":
    import msvcrt
else:
    import termios
    import tty


def get_password():
    print("Enter database password: ", end="", flush=True)
    password = ""

    if os.name == "nt":
        while True:
            char = msvcrt.getwch()
            if char == "\r":
                print()
                break
            elif char == "\b":
                if password:
                    password = password[:-1]
                    print("\b \b", end="", flush=True)
            elif char == "\003":
                raise KeyboardInterrupt
            else:
                password += char
                print("*", end="", flush=True)
    else:
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            while True:
                char = sys.stdin.read(1)
                if char in ("\r", "\n"):
                    print()
                    break
                elif char in ("\x7f", "\b"):
                    if password:
                        password = password[:-1]
                        print("\b \b", end="", flush=True)
                elif char == "\x03":
                    raise KeyboardInterrupt
                else:
                    password += char
                    print("*", end="", flush=True)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

    return password


def database_is_ready(cursor):
    cursor.execute(
        "SELECT COUNT(*) FROM information_schema.TABLES WHERE TABLE_SCHEMA = %s",
        (DATABASE_NAME,),
    )
    return cursor.fetchone()[0] >= len(TABLES)


def setup_database(host, user, password):
    project_root = Path(__file__).resolve().parent.parent
    sql_path = project_root / "02_Database" / SQL_FILE
    connection = cursor = None

    try:
        connection = mysql.connector.connect(host=host, user=user, password=password)
        cursor = connection.cursor()

        if database_is_ready(cursor):
            print_success("Database setup completed.", indent="")
            print()
            return True

        if not sql_path.is_file():
            print_warning(f"SQL file not found: {sql_path}", indent="")
            return False

        for statement in read_sql_statements(sql_path):
            if statement.upper().startswith("INSERT INTO"):
                table = statement.split()[2].strip("`")
                cursor.execute(f"SELECT COUNT(*) FROM `{table}`")
                if cursor.fetchone()[0] > 0:
                    continue

            cursor.execute(statement)

        connection.commit()
        print_success("Database setup completed.", indent="")
        print()
        return True

    except (mysql.connector.Error, OSError) as error:
        if connection:
            connection.rollback()
        print_error(error, indent="")
        return False

    finally:
        if cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()


BANNER_TITLE = "Company Employee & Project Management System"


def print_banner():
    label = f"   {BANNER_TITLE}   "
    width = len(label)
    print()
    print("┌" + "─" * width + "┐")
    print("│" + label + "│")
    print("└" + "─" * width + "┘")


def main():
    enable_ansi()

    from lib import insert, display, search, report, update, delete, reset

    while True:
        print("┌─────────────────────────┐")
        print("│   Database Connection   │")
        print("└─────────────────────────┘")

        host = input("Enter database host: ").strip()
        user = input("Enter database username: ").strip()
        password = get_password()

        try:
            connection = mysql.connector.connect(host=host, user=user, password=password)
            connection.close()
            break
        except mysql.connector.Error as error:
            if error.errno == 1045:
                print_warning("Access denied. Please try again.", indent="")
            else:
                print_error(error, indent="")
            print()

    if not setup_database(host, user, password):
        print_warning("Database setup failed.", indent="")
        return

    time.sleep(1)

    db_config = {"host": host, "user": user, "password": password, "database": DATABASE_NAME}
    os.system("cls" if os.name == "nt" else "clear")

    actions = {
        "insert": insert.insert,
        "display": display.display,
        "search": search.search,
        "report": report.report,
        "update": update.update,
        "delete": delete.delete,
        "reset": reset.reset,
    }

    print_banner()
    print()

    while True:
        print(f"{BLUE}Available commands: insert / display / search / report / update / delete / reset / clear / quit{RESET}")

        command = input("Choose a command: ").strip().lower()

        if command in actions:
            print(BAR)
            reset_gap()
            actions[command](db_config)
        elif command == "clear":
            os.system("cls" if os.name == "nt" else "clear")
            print_banner()
            print()
            continue
        elif command in ["quit", "q"]:
            print_success("Goodbye!", indent="")
            print()
            time.sleep(1)
            break
        else:
            print_warning("Invalid command. Please try again.", indent="")

        print()


if __name__ == "__main__":
    main()
