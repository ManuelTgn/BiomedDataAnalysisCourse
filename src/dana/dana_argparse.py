"""DANA redefinition of ArgumentParser and HelpFormatter.

The ArgumentParser and HelpFormatter classes are customized to 
assign a different style to the tool's help. When wrong arguments
are given, DANA reminds the user to check the help for further 
explanations on the returned errors. 
"""

from dana.dana import __version__

from argparse import (
    ArgumentParser,
    HelpFormatter,
    Action,
    _ArgumentGroup,
    SUPPRESS
)
from typing import Dict, Iterable, Tuple
from colorama import Fore, init

import sys


class DanaArgumentParser(ArgumentParser):
    """This class extends ArgumentParser from argparse.
    Costumize the default argparse help formatting (replace default
    error message of argparse).

    ...

    Methods
    -------
    error(msg)
        Print error message, when wrong arguments are given.

    """

    class DanaHelpFormatter(HelpFormatter):
        """This class extends HelpFormatter from argparse.
        Customize help format for DANA.
        
        ...

        Methods
        -------
        add_usage(usage, actions, groups, prefix=None)
            Define help style.
        """

        def add_usage(
            self, 
            usage: str, 
            actions: Iterable[Action], 
            groups: Iterable[_ArgumentGroup], 
            prefix: str = ...
        ) -> None:
            if usage is not SUPPRESS:
                self._add_item(self._format_usage, usage, actions, groups, "")

    # end of DanaHelpFormatter

    def __init__(self, *args: Tuple, **kwargs: Dict) -> None:
        kwargs["formatter_class"] = self.DanaHelpFormatter
        kwargs["usage"] = kwargs["usage"].replace("{version", __version__)
        super().__init__(*args, **kwargs)
    
    def error(self, errmsg: str) -> None:
        assert isinstance(errmsg, str)
        errormsg = Fore.RED + "\nERROR: " + "{}." + Fore.RESET + "\n\nRun \"dana --help\" to see usage.\n\n"
        sys.stderr.write(errormsg.format(errmsg))
        sys.exit(3)

    def error_noargs(self) -> None:
        self.print_help()
        sys.exit(2)

