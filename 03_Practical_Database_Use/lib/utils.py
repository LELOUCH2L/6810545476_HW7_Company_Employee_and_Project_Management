import os
import sys
import time
from contextlib import contextmanager

import mysql.connector  # type: ignore
from mysql.connector import errorcode  # type: ignore


RESET = "\033[0m"
BOLD = "\033[1m"
DIM = "\033[2m"
RED = "\033[38;2;255;85;85m"
GREEN = "\033[38;2;74;222;128m"
YELLOW = "\033[33m"
BLUE = "\033[38;2;55;148;255m"

BAR = f"{DIM}│{RESET}"
INDENT = f"{BAR}   "


def enable_ansi():
    if os.name == "nt":
        try:
            import ctypes
            kernel32 = ctypes.windll.kernel32
            handle = kernel32.GetStdHandle(-11)
            mode = ctypes.c_uint32()
            kernel32.GetConsoleMode(handle, ctypes.byref(mode))
            kernel32.SetConsoleMode(handle, mode.value | 0x0004)
        except Exception:
            pass


_gap_pending = False
_tight = False


@contextmanager
def tight():
    global _tight
    _tight = True
    try:
        yield
    finally:
        _tight = False


def pause(seconds=0.5):
    sys.stdout.flush()
    time.sleep(seconds)


def reset_gap():
    global _gap_pending
    _gap_pending = False


def _flush_gap():
    global _gap_pending
    if _gap_pending:
        print(BAR)
        _gap_pending = False


def _begin_block():
    global _gap_pending
    print(BAR)
    _gap_pending = False


def _end_block():
    global _gap_pending
    _gap_pending = True


def _emit(text, indent=INDENT, result=False):
    if not indent:
        print()
        print(text)
        return
    if result:
        _begin_block()
    else:
        _flush_gap()
    print(f"{indent}{text}")
    if result and not _tight:
        _end_block()


class GoBack(Exception):
    pass


def ask(prompt, key=False):
    _flush_gap()
    line = f"{INDENT}{prompt} (or 'back'): "
    value = input(line).strip()
    if key and value.lower() != "back":
        value = value.upper()
        if sys.stdout.isatty():
            print(f"\033[1A\r\033[K{line}{value}")
    if not _tight or value.lower() == "back":
        _end_block()
    if value.lower() == "back":
        raise GoBack()
    return value


def match_option(raw, options):
    text = raw.strip().lower()
    if not text:
        return None
    if text.isdecimal():
        number = int(text)
        return options[number - 1] if 1 <= number <= len(options) else None
    for option in options:
        if option.lower() == text:
            return option
    starts = [option for option in options if option.lower().startswith(text)]
    return starts[0] if len(starts) == 1 else None


def choose(options, heading, prompt):
    if heading:
        print_info(heading)
    for i, option in enumerate(options, start=1):
        _emit(f"{BLUE}{i}. {option}{RESET}")
    while True:
        picked = match_option(ask(prompt), options)
        if picked:
            return picked
        print_warning("Invalid selection.")


def confirm(prompt="Are you sure?"):
    return choose(["Yes", "No"], None, prompt) == "Yes"


def print_info(message, indent=INDENT):
    _emit(f"{BLUE}{message}{RESET}", indent)


def print_caution(message, indent=INDENT):
    _emit(f"{YELLOW}> {message}{RESET}", indent)


def print_warning(message, indent=INDENT):
    _emit(f"{RED}> {message}{RESET}", indent, result=True)


def print_success(message, indent=INDENT):
    _emit(f"{GREEN}> {message}{RESET}", indent, result=True)


def print_error(error, indent=INDENT):
    _emit(f"{RED}> {format_mysql_error(error)}{RESET}", indent, result=True)


def print_table(columns, rows, title=None, note=None):
    _begin_block()
    if title:
        print(f"{INDENT}{BLUE}{title}{RESET}")

    if not rows:
        print(f"{INDENT}{RED}> No records found.{RESET}")
    else:
        widths = [len(str(col)) for col in columns]
        for row in rows:
            for i, value in enumerate(row):
                widths[i] = max(widths[i], len(str(value)))

        def format_row(values, bold=False):
            style = BOLD if bold else ""
            end = RESET if bold else ""
            cells = f" {DIM}│{RESET} ".join(f"{style}{str(v).ljust(widths[i])}{end}" for i, v in enumerate(values))
            return f"{INDENT}{DIM}│{RESET} {cells} {DIM}│{RESET}"

        def separator(left, middle, right):
            return f"{INDENT}{DIM}" + left + middle.join("─" * (w + 2) for w in widths) + right + RESET

        print(separator("┌", "┬", "┐"))
        print(format_row(columns, bold=True))
        print(separator("├", "┼", "┤"))
        for row in rows:
            print(format_row(row))
        print(separator("└", "┴", "┘"))

    if note:
        print(f"{INDENT}{note}")
    _end_block()


def get_connection(db_config):
    try:
        return mysql.connector.connect(**db_config)
    except mysql.connector.Error as error:
        if error.errno == errorcode.ER_BAD_DB_ERROR:
            raise mysql.connector.Error(
                f"Database '{db_config['database']}' not found. Try resetting the database with the reset command."
            ) from None
        raise


def format_mysql_error(error):
    if isinstance(error, mysql.connector.Error) and getattr(error, "errno", None):
        sqlstate = f" ({error.sqlstate})" if getattr(error, "sqlstate", None) else ""
        return f"ERROR {error.errno}{sqlstate}: {error.msg}"
    return f"ERROR: {error}"


def read_sql_statements(path):
    with open(path, "r", encoding="utf-8") as file:
        lines = [line for line in file if not line.lstrip().startswith("--")]
    return [statement.strip() for statement in "".join(lines).split(";") if statement.strip()]
