"""DANA utilities"""

from typing import Callable
from colorama import Fore

import csv
import sys
import os


def exception_handler(
    exception_type: Callable[[Exception], None], 
    errmsg: str, 
    debug: bool
) -> None:
    """Handle exception for debugging purposes. Gracefully exit 
    from errors raised. If debug is set to True, the entire error 
    stack is printed to stderr.
    """
    assert isinstance(errmsg, str)
    if debug:
        raise exception_type(f"\n\n{errmsg}")
    sys.stderr.write(Fore.RED + f"\n\nERROR: {errmsg}\n" + Fore.RESET)

def is_csv(csvfile: str, debug: bool = False) -> bool:
    if not isinstance(csvfile, str):
        errmsg = f"Expected {str.__name__}, got {type(csvfile).__name__}"
        exception_handler(TypeError, errmsg, debug)
    if not os.path.isfile(csvfile):
        errmsg = f"Unable to locate {csvfile}"
        exception_handler(FileNotFoundError, errmsg, debug)
    handle = open(csvfile, mode="rb")
    try:
        # Perform various checks on the dialect (e.g., lineseparator,
        # delimiter) to make sure it's sane 
        # (see https://stackoverflow.com/questions/2984888/check-if-file-has-a-csv-format-with-python)
        dialect = csv.Sniffer().sniff(handle.read(1024))
        handle.seek(0)  # reset file pointer
    except:
        return False  # not CSV
    return True  # CSV parsing went fine
