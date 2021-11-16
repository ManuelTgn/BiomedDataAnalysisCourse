from utils import (
    exception_handler,
    check_type
)

from typing import Dict

import pandas as pd
import numpy as np

import sys
import os


def csv_reader(
    csv_file: str, 
    separator: str, 
    debug: bool,
    **kwargs: Dict
) -> pd.DataFrame:
    check_type(str, csv_file, debug)
    if not os.path.isfile(csv_file):
        errmsg = f"Unable to locate {csv_file}"
        exception_handler(FileNotFoundError, errmsg, debug)
    check_type(str, separator, debug)
    if not separator:
        errmsg = f"Forbidden separator ({separator})"
        exception_handler(ValueError, errmsg, debug)
    df = pd.read_csv(csv_file, sep=separator, **kwargs)
    assert not df.empty  # check that dataframe is not empty
    return df



