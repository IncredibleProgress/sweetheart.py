"""
Sweetheart
a supercharged heart for the non-expert hands
"""

__version__ = "0.1.2"
__license__ = "CeCILL-C FREE SOFTWARE LICENSE AGREEMENT"
__author__ = "Nicolas Champion <champion.nicolas@gmail.com>"


from os import getenv
if not getenv('SWSLVL'):
    print(f"Thanks for using Sweetheart !")

# default dir/module name of master project
#FIXME: allow replacing sweetheart by a fork of it
MASTER_MODULE = "sweetheart"
