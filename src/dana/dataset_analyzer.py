"""DANA analysis core functions.
"""
from utils import exception_handler, check_type

from sklearn.metrics.pairwise import euclidean_distances
from sklearn.preprocessing import OneHotEncoder
from xlsxwriter.worksheet import Worksheet
from xlsxwriter.workbook import Workbook
from typing import Dict, List, Tuple
from numpy import ndarray

import pandas as pd
import numpy as np

import string
import os


def csv_reader(
    csv_file: str, separator: str, debug: bool, **kwargs: Dict
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
    dataset: pd.DataFrame, debug: bool = False, verbose: bool = False
) -> Tuple[int, int]:
    check_type(pd.DataFrame, dataset, debug)
    assert not dataset.empty
    nrow, ncol = dataset.shape
    assert nrow > 0 and ncol > 0
    return nrow, ncol


def compute_column_type(
    dataset: pd.DataFrame, debug: bool, verbose: bool
) -> Dict[str, str]:
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
    dataset: pd.DataFrame, debug: bool, verbose: bool
) -> Dict[str, Dict[str, str]]:
    check_type(pd.DataFrame, dataset, debug)
    if dataset.empty:
        errmsg = f"Empty {pd.DataFrame.__name__} object; unable to print statistics"
        exception_handler(ValueError, errmsg, debug)
    column_types = compute_column_type(dataset, debug, verbose)
    cols = dataset.columns.tolist()
    columns_stats = {}  # dictionary with columns statistics
    for col in cols:
        counts = dataset[col].value_counts().to_dict()
        indexes = list(counts.keys())
        values = np.array(list(counts.values()))
        unique_vals_num = len(indexes)
        most_freq_val = indexes[int(np.where(values == values.max())[0])]
        less_freq_val = indexes[int(np.where(values == values.min())[0])]
        columns_stats[col] = {
            "type": column_types[col],
            "index": indexes,
            "counts": ["%.2f%%" % (val * 100) for val in (values / values.sum())],
            "values_num": unique_vals_num,
            "most_freq": most_freq_val,
            "less_freq": less_freq_val,
        }
        assert len(columns_stats[col]["index"]) == len(columns_stats[col]["counts"])
    return columns_stats


def print_statistics(dataset: pd.DataFrame, debug: bool, verbose: bool) -> None:
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
                f"\t- Variable type: {columns_stat[col]['type']}\n"
                "\t- Values:"
            )
        )
        indexes = columns_stat[col]["index"]
        values = columns_stat[col]["counts"]
        for i, idx in enumerate(indexes):
            print(f"\t\t- {idx}: {values[i]}")


def format_excel_column(
    df: pd.DataFrame,
    workbook: Workbook,
    worksheet: Worksheet,
    columns: List[str],
    colors: Dict[str, str],
    col_type: str,
    excel_headers: Dict[int, str],
    debug: bool = False,
    verbose: bool = False,
) -> None:
    check_type(pd.DataFrame, df, debug)
    if df.empty:
        errmsg = f"Empty {pd.DataFrame.__name__} object; unable to write statistics"
        exception_handler(ValueError, errmsg, debug)
    check_type(Workbook, workbook, debug)
    check_type(Worksheet, worksheet, debug)
    check_type(list, columns, debug)
    check_type(dict, colors, debug)
    check_type(str, col_type, debug)
    check_type(dict, excel_headers, debug)
    try:
        color = colors[col_type]
    except IndexError as e:
        errmsg = f"Unrecognized column type to color ({col_type})"
        exception_handler(e, errmsg, debug)
    for col in columns:
        frmt = workbook.add_format({"bg_color": color})
        excel_header = str(excel_headers[df.columns.get_loc(col)])
        worksheet.conditional_format(
            excel_header + "2:" + excel_header + str(df.shape[0] + 1),
            {"type": "no_blanks", "format": frmt},
        )


def write_summary_statistics_excel(
    dataset: pd.DataFrame, outdir: str, debug: bool = False, verbose: bool = False
) -> None:
    check_type(pd.DataFrame, dataset, debug)
    if dataset.empty:
        errmsg = f"Empty {pd.DataFrame.__name__} object; unable to write statistics"
        exception_handler(ValueError, errmsg, debug)
    check_type(str, outdir, debug)
    columns_stats = compute_count_stats(dataset, debug, verbose)
    df = {}
    for col in columns_stats.keys():
        df[col] = {
            "var_type": columns_stats[col]["type"],
            "values_number": columns_stats[col]["values_num"],
            "most_frequent_value": columns_stats[col]["most_freq"],
            "less_frequent_value": columns_stats[col]["less_freq"],
        }
    df = pd.DataFrame(df)
    # write excel report
    outfile = os.path.join(outdir, "summary.xlsx")
    writer = pd.ExcelWriter(outfile, engine="xlsxwriter")
    df.to_excel(writer, sheet_name="Sheet1")
    workbook = writer.book
    worksheet = writer.sheets["Sheet1"]
    # color columns according to variable type
    excel_header_dict = dict(
        zip(range(25), list(string.ascii_uppercase)[1:])
    )  # skip column 'A' (index col)
    # recover numerical and categorical columns
    df_t = df.T
    cat_cols = df_t[df_t.var_type == "categorical"].index.tolist()
    num_cols = df_t[df_t.var_type == "numerical"].index.tolist()
    colors = {"categorical": "#68AB25", "numerical": "#9F25AB"}  # columns' colors
    # format categorical columns
    format_excel_column(
        df,
        workbook,
        worksheet,
        cat_cols,
        colors,
        "categorical",
        excel_header_dict,
        debug,
        verbose,
    )
    # format numerical columns
    format_excel_column(
        df,
        workbook,
        worksheet,
        num_cols,
        colors,
        "numerical",
        excel_header_dict,
        debug,
    )
    writer.save()


def compute_euclidean_distance(
    dataset: pd.DataFrame, debug: bool, verbose: bool
) -> ndarray:
    check_type(pd.DataFrame, dataset, debug)
    if dataset.empty:
        errmsg = f"Empty {pd.DataFrame.__name__} object; unable to write statistics"
        exception_handler(ValueError, errmsg, debug)
    enc = OneHotEncoder(handle_unknown="ignore")
    enc.fit(dataset)
    ohc_data = enc.transform(dataset).toarray()
    dist_mat = euclidean_distances(ohc_data)
    return dist_mat
