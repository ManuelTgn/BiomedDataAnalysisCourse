from dana.utils import exception_handler

from argparse import Namespace

import sys
import os

__version__ = "0.0.1"


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


def print_close(start: float, stop: float) -> None:
    