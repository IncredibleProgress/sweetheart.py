"""
get-sweetheart.py: the Sweetheart Shell installer via Github
this requires sudo permissions to provide the 'sws' basic features
"""

import os,sys,stat,json
from typing import List
from subprocess import run

__version__  = "0.1.5b"
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

    # bin paths settings
    BIN = (f"{os.environ['HOME']}/.local/bin","/usr/local/bin","/usr/bin","/bin")
    PTH = [path for path in BIN if path in os.environ["PATH"]]
    EXECUTABLES = {} # fetched by list_executables()
    MISSING = [] # fetched by list_executables()

    @staticmethod
    def list_executables(executables:str) -> List[str]:
        # check executables availability 
        for cmd in executables.split():
            paths= [p for p in Path.PTH if os.path.isfile(f"{p}/{cmd}")]
            version = bash_stdout(f"{cmd} --version")

            if paths: Path.EXECUTABLES.update({
                # str pattern -> "cdm::path::version"
                cmd: f"{cmd}::{paths[0]}::{version}" })

        # build the missing list
        Path.MISSING = [m for m in executables.split() if m not in Path.EXECUTABLES]
        # return list of executables
        return list(Path.EXECUTABLES)

class Poetry:

    # poetry commands settings
    INIT = f"{Path.BIN[0]}/poetry init -n"
    ADD = f"{Path.BIN[0]}/poetry add sweetheart"
    ENV_PATH = f"{Path.BIN[0]}/poetry env info --path"
    INSTALL = "curl -sSL https://install.python-poetry.org | python3 -"

# facility for getting bash standard output
bash_stdout = lambda cmd: \
    run(cmd,text=True,capture_output=True,shell=True).stdout.strip()

# get distrib infos on debian/ubuntu
distrib = bash_stdout("lsb_release -is").lower()
codename = bash_stdout("lsb_release -cs").lower()
executables = Path.list_executables("apt curl cargo node npm python3 poetry")

print(
    "\n[SWEETHEART] checking prerequisites :",
    "\n current running system :",distrib.capitalize(),codename.capitalize(),
    "\n missing executables:",Path.MISSING,"\n")

# diagnose and set operating system
if "apt" not in executables:
    print("WARNING you are not running on Ubuntu/Debian derivated system",
    "which is not supported by this script for installing OS requirements")
    sys.exit(1)

if "curl" not in executables:
    run("sudo apt install curl",shell=True)

if "cargo" not in executables:
    run("sudo apt install cargo",shell=True)

if "node" not in executables and "npm" not in executables:
    print("install NodeJS 16.x LTS from nodesource.com ...")
    run("curl -fsSL https://deb.nodesource.com/setup_16.x | sudo -E bash -",shell=True)
    run("sudo apt install -y nodejs",shell=True)

if "poetry" not in executables:
    print("poetry has to be installed for managing Python's envs and libs")
    run("sudo apt install python3-venv",shell=True)
    run(Poetry.INSTALL,shell=True)

# make required directories
os.makedirs(Path.CONFIG,exist_ok=True)
os.makedirs(Path.SCRIPTS,exist_ok=True)
os.makedirs(Path.PYTHON,exist_ok=True)

# build my_python directory
os.chdir(Path.PYTHON)
run(Poetry.INIT,shell=True)
run(Poetry.ADD,shell=True)

# set python env
venv = bash_stdout(Poetry.ENV_PATH)
if venv=="": raise Exception("Error, no Python env found")

# check and update executables
Path.EXECUTABLES.pop('curl')
Path.list_executables("python3 poetry cargo npm")
print(
    "\n[SWEETHEART] show executables :",
    *Path.EXECUTABLES.values(), sep="\n ")

# set subroc.conf
with open(Path.SUBPROC,"w") as file_out:
    json.dump({
        'pyenv': venv,
        'executables': Path.EXECUTABLES },file_out)

# set RethinkDB repository
if not bash_stdout("apt policy rethinkdb"):
    for instruc in f"""

echo WARNING: sudo permission is required for installing the RethinkDB repository
echo "deb https://download.rethinkdb.com/repository/{distrib}-{codename} {codename} main" | sudo tee /etc/apt/sources.list.d/rethinkdb.list
wget -qO- https://download.rethinkdb.com/repository/raw/pubkey.gpg | sudo apt-key add -
sudo apt-get update """.splitlines(): run(instruc.strip(),shell=True)

# set the sws command (faster than 'poetry run')
with open(Path.SWS,"w") as file_out:
    file_out.write(f"""

#!/bin/sh
{venv}/bin/python3 -m sweetheart.sweet sh $* """.strip())
os.chmod(Path.SWS,stat.S_IRWXU|stat.S_IRGRP|stat.S_IROTH)

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
print(
    f"\n[SWEETHEART] Welcome {os.environ['USER'].capitalize()} !",
    " the 'sws --init' command is now available after restarting bash",
    " all done setting Sweetheart requirements\n",sep="\n")
