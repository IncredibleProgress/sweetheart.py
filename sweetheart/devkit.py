
from sweetheart import *

class git:
    """ Coming Soon """
    pass

class poetry:
    """ Coming Soon """
    pass

def enforce_dev_links():

    src = f"{BaseConfig.HOME}/{MASTER_MODULE}.py"# source dir
    pjt = f"{BaseConfig.HOME}/.sweet/{MASTER_MODULE}"# project dir

    # make links for testing dev files
    enforced_symlink(
        f"{src}/configuration/packages.json",
        f"{pjt}/configuration/packages.json" )
    enforced_symlink(
        f"{src}/webpages/resources/tailwind.base.css",
        f"{pjt}/webpages/resources/tailwind.base.css" )
    enforced_symlink(
        f"{src}/webpages/resources/tailwind.config.js",
        f"{pjt}/webpages/resources/tailwind.config.js" )
    enforced_symlink(
        f"{src}/webpages/HTML",
        f"{pjt}/webpages/HTML" )

    # make links for testing dev directories
    enforced_symlink(
        f"{src}/webpages/templates",
        f"{pjt}/webpages/templates" )
    enforced_symlink(
        f"{src}/documentation/sweetdoc",
        f"{pjt}/documentation/sweetdoc" )
    enforced_symlink(
        f"{src}/documentation/notebooks",
        f"{pjt}/documentation/notebooks" )


def enforce_sweetheart_local_source():
    # link ~/sweetheart.py as python package
    set_config()
    sp.poetry("remove","sweetheart")

    enforced_symlink(f"{BaseConfig.HOME}/{MASTER_MODULE}.py",
        f"{BaseConfig._.python_env}/lib/python*/site-packages/sweetheart")

