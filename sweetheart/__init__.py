"""
Sweetheart
a supercharged heart for the non-expert hands
"""

__version__ = "0.1.2"
__license__ = "CeCILL-C FREE SOFTWARE LICENSE AGREEMENT"
__author__ = "Nicolas Champion <champion.nicolas@gmail.com>"

# default dir/module name of master project
#FIXME: allow replacing sweetheart by a fork of it
MASTER_MODULE = "sweetheart"

from sys import argv
from os import getenv

set_msg = "--version" not in argv and "-V" not in argv

if set_msg and not getenv('SWSLVL'):
    # set welcome message
    print(
        f"Thanks for using Sweetheart ",__version__," !\n",
        __license__, sep="" )
