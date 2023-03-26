

def symlink(source,dest):

    import shutil

    if os.path.islink(dest): print(f"Warning, existing link {dest}")
    elif os.path.isfile(dest): os.remove(dest)
    elif os.path.isdir(dest) : shutil.rmtree(dest)
    try: os.symlink(source,dest)
    except: pass


def dev_links():

    src = f"{BaseConfig.HOME}/{MASTER_MODULE}.py"# source dir
    pjt = f"{BaseConfig.HOME}/.sweet/{MASTER_MODULE}"# project dir

    # make links for testing dev files
    symlink(f"{src}/configuration/packages.json",f"{pjt}/configuration/packages.json")
    symlink(f"{src}/webpages/resources/tailwind.base.css",f"{pjt}/webpages/resources/tailwind.base.css")
    symlink(f"{src}/webpages/resources/tailwind.config.js",f"{pjt}/webpages/resources/tailwind.config.js")
    symlink(f"{src}/webpages/HTML",f"{pjt}/webpages/HTML")

    # make links for testing dev directories
    symlink(f"{src}/webpages/templates",f"{pjt}/webpages/templates")
    symlink(f"{src}/documentation/sweetdoc",f"{pjt}/documentation/sweetdoc")
    symlink(f"{src}/documentation/notebooks",f"{pjt}/documentation/notebooks")


def dev_sweetheart():
    # link ~/sweetheart.py as python package
    set_config()
    sp.poetry("remove","sweetheart")

    symlink(f"{BaseConfig.HOME}/{MASTER_MODULE}.py",
        f"{BaseConfig._.python_env}/lib/python*/site-packages/sweetheart")

