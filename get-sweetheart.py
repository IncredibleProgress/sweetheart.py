"""
get-sweetheart.py: the Github sweetheart installer
allows installation of SWeetheart Shell (sws) basic features
NOTE: this script has been tested on Ubuntu 20.04 only

2 optionnal arguments requiring sudo permissions are provided:
    --rethinkdb :   set the official deb repository for getting RethinkDB
    --local-bin :   set symbolic link to sws within /usr/local/bin
"""
import os,sys,stat,json
from subprocess import run

__version__  = "0.1.3"

# paths setting
PATHS = {
    'config': f"{os.environ['HOME']}/.sweet/sweetheart/configuration",
    'scripts': f"{os.environ['HOME']}/.sweet/sweetheart/programs/scripts",
    'python': f"{os.environ['HOME']}/.sweet/sweetheart/programs/my_python" }

# make required directories
for basedir in PATHS.items():
    os.makedirs(basedir,exist_ok=True)

# for getting bash standard output
bash_stdout = lambda cmd:\
    run(cmd,text=True,capture_output=True,shell=True).stdout.strip()

# get distrib infos on debian/ubuntu
distrib = bash_stdout("lsb_release -is").lower()
codename = bash_stdout("lsb_release -cs").lower()

# poetry commands
POETRY_BIN = f"{os.environ['HOME']}/.local/bin/poetry"
POETRY_INSTALL = "curl -sSL https://install.python-poetry.org | python3 -"
POETRY_INIT = f"{os.environ['HOME']}/.local/bin/poetry init -n"
POETRY_ADD = f"{os.environ['HOME']}/.local/bin/poetry add sweetheart"

# python-poetry is required
if not os.path.isfile(POETRY_BIN):
    run(POETRY_INSTALL,shell=True)

# create python directories
os.makedirs(PATHS["python"],exist_ok=True)
os.chdir(PATHS["python"])
run(POETRY_INIT,shell=True)
run(POETRY_ADD,shell=True)

# set python env
venv = bash_stdout(f"{POETRY_BIN} env info --path")
if venv == "": raise Exception("Error, no python env found")

# set subroc.conf
with open(f"{PATHS['config']}/subproc.json","w") as file_out:
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
with open(f"{PATHS['scripts']}/sws","w") as file_out:
    file_out.write(f"""

#!/bin/sh
#NOTE: much faster than 'poetry run'
{venv}/bin/python3 -m sweetheart.sweet sh $*

    """.strip())

os.chmod(f"{PATHS['scripts']}/sws",stat.S_IRWXU|stat.S_IRGRP|stat.S_IROTH)
print(f"\n[SWEETHEART] Welcome {os.environ['USER'].capitalize()} !",
    f"\nthe 'sws' command is now available for {distrib} {codename}")

if '--local-bin' in sys.argv:
    run(f"sudo ln -s {PATHS['scripts']}/sws /usr/local/bin/",shell=True)

elif not PATHS['scripts'] in os.environ['PATH']:
    with open(f"{os.environ['HOME']}/.bashrc","a") as fi:
        fi.write(f"\nexport PATH={PATHS['scripts']}:$PATH")
        print(f"{PATHS['scripts']} added to $PATH within ~./bashrc")

# exit message
print("\n[SWEETHEART] all done setting Sweetheart requirements",
    "\nif needed set 'config.json' and 'subproc.json' within configuration directory",
    "\nthen restart bash and type 'sws --init' for installing usual components",
    end="\n\n")
