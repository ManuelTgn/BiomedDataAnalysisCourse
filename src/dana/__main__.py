# MIT License
# Copyright (c) 2021 ManuelTgn
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

"""
DANA version {version}

Usage:

bla bla

Run dana --help to see all command line options.
"""

from dana import (
    dana,
    __version__
)
from utils import (
    check_type,
    is_csv,
    DEFAULT_SEPARATOR
)
from dana_argparse import DanaArgumentParser

import random, threading, webbrowser

from typing import Optional, List

import time
import sys
import os


def get_parser() -> DanaArgumentParser:
    parser = DanaArgumentParser(usage=__doc__, add_help=False)
    # start command line args parsing
    group = parser.add_argument_group("Options")
    group.add_argument(
        "-h", 
        "--help", 
        action="help", 
        help="Show this message and exit."
    )
    group.add_argument(
        "--version", 
        action="version", 
        help="Print DANA version and exit.", 
        version=__version__
    )
    group.add_argument(
        "--verbose",
        default=False,
        action="store_true",
        help="Print verbose messages during analysis execution."
    )
    group.add_argument(
        "--debug",
        default=False,
        action="store_true",
        dest="debug",
        help="Enable error stack tracing for debugging."
    )
    group.add_argument(
        "-f",
        "--func",
        type=str,
        nargs="?",
        default="analyze",
        metavar="ACTION",
        help="Available functions (\"analyze\" or \"introduce\")" 
    )
    group.add_argument(
        "-d", 
        "--dataset", 
        type=str, 
        nargs="?", 
        default="", 
        metavar="DATASET",
        help="Path to the dataset CSV file."
    )
    group.add_argument(
        "-s",
        "--separator",
        type=str,
        nargs="?",
        const=DEFAULT_SEPARATOR,
        default=DEFAULT_SEPARATOR,
        metavar="SEPARATOR",
        help="Separator character used in the input dataset"
    )
    group.add_argument(
        "-o",
        "--out",
        type=str,
        nargs="?",
        default="./",
        metavar="OUTFILE",
        help="Path to summary statistics excel file. Used with \"analyze\" function."
    )
    group.add_argument(
        "--pid",
        type=int,
        nargs="?",
        default=None,
        metavar="PID",
        help="Patient ID. Used with \"introduce\" function."
    )
    return parser


def main(commandline_args: Optional[List[str]]=None) -> None:
    parser = get_parser()
    if commandline_args is None:
        commandline_args = sys.argv[1:]  # get input args
    if not commandline_args:  # no args given
        parser.error_noargs()
    args = parser.parse_args(commandline_args)  # parse arguments
    
    # --- read command line args
    if not isinstance(args.verbose, bool):
        errmsg = f"Expected {bool.__name__}, got {type(args.verbose).__name__}"
        parser.error(errmsg)
    verbose = args.verbose
    if not isinstance(args.debug, bool):
        errmsg = f"Expected {bool.__name__}, got {type(args.debug).__name__}"
        parser.error(errmsg)
    debug = args.debug
    if not args.func:
        parser.error(
            "No function selected. Please choose one between \"analyze\" and \"introduce\""
        )
    check_type(str, args.func)
    if args.func != "analyze" and args.func != "introduce":
        parser.error(
            "Unknown function selected. Please choose one between \"analyze\" and \"introduce\""
        )
    if not args.dataset:
        parser.error("No dataset file given")
    check_type(str, args.separator)
    if not is_csv(args.dataset, args.separator):
        parser.error(f"{args.dataset} does not appear to be a CSV file")

    # check args consistency with the chosen functionality
    if args.func == "analyze":
        if args.pid is not None:
            parser.error(
                "Forbidden argument given (\"--pid\") with functionality \"analyze\""
            )
        check_type(str, args.out, debug)
        if not args.out:
            parser.error("Missing output summary statistics file")
    if args.func == "introduce":
        if args.out:
            parser.error(
                "Forbidden argument given (\"--out\") with functionality \"introduce\""
            )

    # DANA analysis
    dana(args, verbose, debug)


if __name__ == "__main__":
    main()
    


