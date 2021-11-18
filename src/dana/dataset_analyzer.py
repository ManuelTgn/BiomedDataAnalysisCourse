from utils import (
    exception_handler,
    check_type
)

from typing import Dict, List, Tuple

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


def compute_shape(
    dataset: pd.DataFrame, 
    debug: bool = False, 
    verbose: bool = False
) -> Tuple[int, int]:
    check_type(pd.DataFrame, dataset, debug)
    assert not dataset.empty
    nrow, ncol = dataset.shape
    assert nrow > 0 and ncol > 0
    return nrow, ncol


def compute_column_type(dataset: pd.DataFrame, debug: bool, verbose: bool) -> Dict[str, str]:
    check_type(pd.DataFrame, dataset)
    if dataset.empty:
        errmsg = f"Empty {pd.DataFrame.__name__} object; unable to print statistics"
        exception_handler(ValueError, errmsg, debug)
    column_types = {}
    # recover numerical columns
    numerical_cols = dataset._get_numeric_data().columns.tolist()
    for num_col in numerical_cols: 
        column_types[num_col] = "numerical"
    # remaining columns are categorical
    categorical_columns = set(dataset.columns.tolist()) - set(numerical_cols)
    for cat_col in categorical_columns:
        column_types[cat_col] = "categorical"
    assert len(column_types.keys()) == dataset.shape[1]
    return column_types


def compute_count_stats(
    dataset: pd.DataFrame,  
    debug: bool, 
    verbose: bool
) -> None:
    check_type(pd.DataFrame, dataset, debug)
    if dataset.empty:
        errmsg = f"Empty {pd.DataFrame.__name__} object; unable to print statistics"
        exception_handler(ValueError, errmsg, debug)
    column_types = compute_column_type(dataset, debug, verbose)
    cols = dataset.columns.tolist()
    columns_stats = {}  # dictionary with columns statistics
    for col in cols:
        counts = dataset[col].value_counts().to_dict()
        indexes = counts.keys()
        values = np.array(list(counts.values()))
        columns_stats[col] = {
            "type":column_types[col], 
            "index":indexes, 
            "counts":["%.2f%%" % (val * 100) for val in (values / values.sum())]
        }
        assert len(columns_stats[col]["index"]) == len(columns_stats[col]["counts"])
    return columns_stats
    

def print_statistics(dataset: pd.DataFrame, debug: bool, verbose: bool)-> None:
    check_type(pd.DataFrame, dataset, debug)
    if dataset.empty:
        errmsg = f"Empty {pd.DataFrame.__name__} object; unable to print statistics"
        exception_handler(ValueError, errmsg, debug)
    dims = compute_shape(dataset, debug, verbose)
    print(f"There are {dims[0]} rows and {dims[1]} columns.")
    columns_stat = compute_count_stats(dataset, debug, verbose)
    for col in columns_stat.keys():
        print(
            str(
                f"{col}:\n"
                f"\t-Variable type: {columns_stat[col]['type']}\n"
                "\t-Values:"
            )
        )
        indexes = columns_stat[col]["index"]
        values = columns_stat[col]["counts"]
        for i,idx in enumerate(indexes):
            print(f"\t\t-{idx}: {values[i]}")

