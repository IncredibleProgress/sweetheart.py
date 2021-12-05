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

__version__  = "0.1.2"

# paths setting
POETRY_BIN = f"{os.environ['HOME']}/.poetry/bin/poetry"
CONFIG_PATH = f"{os.environ['HOME']}/.sweet/sweetheart/configuration"
SWS_PATH = f"{os.environ['HOME']}/.sweet/sweetheart/programs/scripts"

# for getting bash standard output
bash_stdout = lambda cmd:\
    run(cmd,text=True,capture_output=True,shell=True).stdout.strip().lower()

# get distrib infos on debian/ubuntu
distrib = bash_stdout("lsb_release -is")
codename = bash_stdout("lsb_release -cs")

# python-poetry is required
if not os.path.isfile(POETRY_BIN):
    run("curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python3 -",
        shell=True)

# create python directories
os.makedirs(SWS_PATH,exist_ok=True)
os.chdir(f"{SWS_PATH}/..")
run([POETRY_BIN,"new","my_python"])

# install python dependencies
os.chdir("./my_python")
run([POETRY_BIN,"add","sweetheart"])

# set python env
venv = run([POETRY_BIN,"env","info","--path"],
    text=True,capture_output=True).stdout.strip()
if venv == "":
    raise Exception("Error, no python env found")

# set subroc.conf
os.makedirs(CONFIG_PATH,exist_ok=True)
with open(f"{CONFIG_PATH}/subproc.json","w") as file_out:
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
with open(f"{SWS_PATH}/sws","w") as file_out:
    file_out.write(f"""

#!/bin/sh
#NOTE: much faster than 'poetry run'
{venv}/bin/python3 -m sweetheart.sweet sh $*

    """.strip())

os.chmod(f"{SWS_PATH}/sws",stat.S_IRWXU|stat.S_IRGRP|stat.S_IROTH)
print(f"\n[SWEETHEART] Welcome {os.environ['USER'].capitalize()} !",
    f"\nthe 'sws' command is now available for {distrib} {codename}")

if '--local-bin' in sys.argv:
    run(f"sudo ln -s {SWS_PATH}/sws /usr/local/bin/",shell=True)

elif not SWS_PATH in os.environ['PATH']:
    with open(f"{os.environ['HOME']}/.bashrc","a") as fi:
        fi.write(f"\nexport PATH={SWS_PATH}:$PATH")
        print(f"{SWS_PATH} added to $PATH within ~./bashrc")

# exit message
print("\n[SWEETHEART] all done setting Sweetheart requirements",
    "\nif needed set 'config.json' and 'subproc.json' within configuration directory",
    "\nthen restart bash and type 'sws sweet --init' for installing provided components",
    end="\n\n")
