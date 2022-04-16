"""
get-sweetheart.py: the Github sweetheart installer
allows installation of SWeetheart Shell (sws) basic features

optionnal arguments requiring sudo permissions are provided:
    --python-venv : install python3-venv package which is required
    --rethinkdb :   set the official deb repository for getting RethinkDB
    --local-bin :   set symbolic link to sws within /usr/local/bin
    --init-sws  :   run 'sws --init' for getting sweetheart base components
    --init-jpy  :   run 'sws --init jupyterlab' for base components with JupyterLab

NOTE: this script has been tested on Ubuntu 20.04
"""

import os,sys,stat,json
from subprocess import run

__version__  = "0.1.4"
__author__ = "champion.nicolas@gmail.com"
__licence__ = "CeCILL-C FREE SOFTWARE LICENSE AGREEMENT"

class Path:

    # basedirs paths settings
    CONFIG = f"{os.environ['HOME']}/.sweet/sweetheart/configuration"
    SCRIPTS = f"{os.environ['HOME']}/.sweet/sweetheart/programs/scripts"
    PYTHON = f"{os.environ['HOME']}/.sweet/sweetheart/programs/my_python"

    # files paths settings
    SWS = f"{SCRIPTS}/sws"
    SUBPROC = f"{CONFIG}/subproc.json"
    BASHRC = f"{os.environ['HOME']}/.bashrc"

# make required directories
os.makedirs(Path.CONFIG,exist_ok=True)
os.makedirs(Path.SCRIPTS,exist_ok=True)
os.makedirs(Path.PYTHON,exist_ok=True)

class Poetry:

    # poetry commands settings
    BIN = f"{os.environ['HOME']}/.local/bin/poetry"
    INIT = f"{os.environ['HOME']}/.local/bin/poetry init -n"
    ADD = f"{os.environ['HOME']}/.local/bin/poetry add sweetheart"
    INSTALL = "curl -sSL https://install.python-poetry.org | python3 -"
    GET_VENV = "sudo apt install python3-venv"
    ENV_PATH = f"{BIN} env info --path"

# for getting bash standard output
bash_stdout = lambda cmd:\
    run(cmd,text=True,capture_output=True,shell=True).stdout.strip()

# get distrib infos on debian/ubuntu
distrib = bash_stdout("lsb_release -is").lower()
codename = bash_stdout("lsb_release -cs").lower()

# python-poetry is required
if "--python-venv" in sys.argv:
    run(Poetry.GET_VENV,shell=True)
if not os.path.isfile(Poetry.BIN):
    run(Poetry.INSTALL,shell=True)

# build python directory
os.chdir(Path.PYTHON)
run(Poetry.INIT,shell=True)
run(Poetry.ADD,shell=True)

# set python env
venv = bash_stdout(Poetry.ENV_PATH)
if venv=="": raise Exception("Error, no python env found")

# set subroc.conf
with open(Path.SUBPROC,"w") as file_out:
    json.dump({'pyenv':venv},file_out)

# set RethinkDB repository
if '--rethinkdb' in sys.argv and distrib in ('ubuntu','debian'):
    for instruc in f"""

echo WARNING: sudo permission is required for installing the RethinkDB repository
echo "deb https://download.rethinkdb.com/repository/{distrib}-{codename} {codename} main" | sudo tee /etc/apt/sources.list.d/rethinkdb.list
wget -qO- https://download.rethinkdb.com/repository/raw/pubkey.gpg | sudo apt-key add -
sudo apt-get update

    """.splitlines(): run(instruc.strip(),shell=True)

# set SWeetheart Shell command -> sws
with open(Path.SWS,"w") as file_out:
    file_out.write(f"""

#!/bin/sh
#NOTE: much faster than 'poetry run'
{venv}/bin/python3 -m sweetheart.sweet sh $*

    """.strip())

os.chmod(Path.SWS,stat.S_IRWXU|stat.S_IRGRP|stat.S_IROTH)
print(f"""\n[SWEETHEART] Welcome {os.environ['USER'].capitalize()} !
the 'sws' command is now available for {distrib} {codename}""")

# export path within .bashrc
with open(Path.BASHRC,"r") as file_in:
    bashrc = file_in.read()

if '--local-bin' in sys.argv:
    run(f"sudo ln -s {Path.SWS} /usr/local/bin/",shell=True)

elif Path.SCRIPTS not in bashrc:
    with open(Path.BASHRC,"a") as file_out:
        file_out.write(f"\nexport PATH={Path.SCRIPTS}:$PATH")
        print(f"{Path.SCRIPTS} added to $PATH within ~./bashrc")

# exit message
print("""\n[SWEETHEART] all done setting Sweetheart requirements
if needed set 'config.json' and 'subproc.json' within configuration directory\n\n""")

# install sweetheart components
if "--init-sws" in sys.argv:
    run("bash sws --init; sws help",shell=True)

elif "--init-jpy" in sys.argv:
    run("bash sws --init jupyterlab; sws help",shell=True)
