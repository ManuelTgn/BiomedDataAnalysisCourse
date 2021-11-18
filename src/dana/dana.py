
from utils import (
    check_type,
    exception_handler
)
from dataset_analyzer import (
    csv_reader, 
    print_statistics,
    write_summary_statistics_excel
)
from patient import (
    build_patients_dict,
    build_patients_ds
)

from plot_data import (
    plot_age_data,
    plot_recovery_data
)

from argparse import Namespace
from typing import Type

import pandas as pd

import time
import sys
import os

__version__ = "0.0.1"


def dana(
    commandline_args: Namespace, 
    verbose: bool = False, 
    debug: bool = False
) -> None:
    check_type(Namespace, commandline_args, debug)
    try:
        dataset = commandline_args.dataset
    except AttributeError as e:
        errmsg = f"Attempt to access unknown {Namespace.__name__} attribute"
        exception_handler(e, errmsg, debug)
    # check parameters consistency
    check_type(str, dataset, debug)
    if not os.path.isfile(dataset):
        errmsg = f"Unable to locate {dataset}"
        exception_handler(FileNotFoundError, errmsg, debug)
    # store command line arguments in vars
    func = commandline_args.func
    dataset = commandline_args.dataset
    separator = commandline_args.separator
    # start analysis
    dana_start = time.time()
    print_welcome(commandline_args, debug, verbose)
    df = csv_reader(dataset, separator, {})
    if func == "analyze":
        print_statistics(df, debug, verbose)
        write_summary_statistics_excel(df, commandline_args.out, debug, verbose)
        plot_age_data(df, commandline_args.out, debug, verbose)
        plot_recovery_data(df, commandline_args.out, debug, verbose)
    elif func == "introduce":
        dana_introduce(df, commandline_args.pid, verbose, debug)

    dana_stop = time.time()
    print_close(dana_start, dana_stop, debug)


def dana_introduce(dataset: pd.DataFrame, pid: int, verbose: bool, debug: bool) -> None:
    try:
        pats_dict = build_patients_dict(dataset, verbose, debug)
        pats = build_patients_ds(dataset, verbose, debug)
    except ValueError as e:
        errmsg = "An error occurred while building the patients dictionary"
        exception_handler(e, errmsg, debug)
    print(pats_dict[pid])
    print(pats[pid])


def print_welcome(
    commandline_args: Namespace,
    debug: bool = False,
    verbose: bool = False
) -> None:
    if not isinstance(commandline_args.dataset, str):
        errmsg = f"Expected {str.__name__}, got {type(commandline_args.dataset).__name__}"
        exception_handler(TypeError, errmsg, debug)
    print("".join(["*" for _ in range(75)]))
    print(f"\n\tWelcome to DANA v{__version__}\n")
    print("".join(["*" for _ in range(75)]))
    analysis_msg = f"Starting DANA analysis on {commandline_args.dataset}.\n"
    if verbose:
        analysis_msg = analysis_msg + str(
            "\n"
            "Parameters:\n"
            f"--dataset: {commandline_args.dataset}\n"
            f"--debug: {commandline_args.debug}\n"
            f"--verbose: {commandline_args.verbose}\n"
        )
    print(analysis_msg)


def print_close(start: float, stop: float, debug: bool = False) -> None:
    check_type(float, start, debug)
    check_type(float, stop, debug)
    if start < 0 or stop < 0:
        errmsg = f"Illegal {float.__name__} value"
        exception_handler(ValueError, errmsg, debug)
    if stop < start:
        errmsg = f"Illegal values (stop: {stop} < start: {start})"
        exception_handler(ValueError, errmsg, debug)
    closing_msg = "DANA analysis finished. \nElapsed time %.2fs" % (stop - start)
    print(closing_msg)
