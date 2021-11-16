"""DANA utilities"""

from typing import Callable, Generic, TypeVar
from colorama import Fore

import pandas as pd

import csv
import sys
import os


DEFAULT_SEPARATOR = ","
NO_GROUP = "0000_nogroup"
PATID_START = 1000000
T = TypeVar("T")  # generic template type


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


def check_type(
    var_type: Generic[T], 
    variable: Generic[T], 
    debug: bool = False
) -> None:
    if not isinstance(variable, var_type):
        errmsg = f"Expected {var_type.__name__}, got {type(variable).__name__}"
        exception_handler(TypeError, errmsg, debug)
    pass  # if type check OK, skip


def is_csv(csvfile: str, separator: str,  debug: bool = False) -> bool:
    check_type(str, csvfile, debug)
    check_type(str, separator)
    if not os.path.isfile(csvfile):
        errmsg = f"Unable to locate {csvfile}"
        exception_handler(FileNotFoundError, errmsg, debug)
    print(separator)
    if separator != DEFAULT_SEPARATOR:
        if pd.read_csv(csvfile, sep=separator).shape[1] <= 1:
            return False
        return True
    else:  # separator == DEFAULT_SEPARATOR
        try:
            handle = open(csvfile, mode="rb")
            # Perform various checks on the dialect (e.g., lineseparator,
            # delimiter) to make sure it's sane 
            # (see https://stackoverflow.com/questions/2984888/check-if-file-has-a-csv-format-with-python)
            dialect = csv.Sniffer().sniff(handle.read(1024))
            handle.seek(0)  # reset file pointer
        except:
            return False  # not CSV
        finally:
            handle.close()
        return True  # CSV parsing went fine
    return False  # should not be reached
