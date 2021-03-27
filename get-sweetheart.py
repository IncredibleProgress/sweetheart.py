"""
get-sweetheart.py: the github sweetheart installer (recommended)
allow installation without any python dependencies matter
"""
import os,stat
from subprocess import run

# paths setting
POETRY_BIN = f"{os.environ['HOME']}/.poetry/bin/poetry"
SWS_PATH = f"{os.environ['HOME']}/.sweet/sweetheart/programs/scripts"

# python-poetry is required
if not os.path.isfile(POETRY_BIN):
    
    run("curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python3 -",
        shell=True)

# create directories
os.makedirs(SWS_PATH,exist_ok=True)
os.chdir(f"{SWS_PATH}/..")
run([POETRY_BIN,"-q","new","my_python"])

# install python dependencies
os.chdir("./my_python")
run([POETRY_BIN,"add","sweetheart"])

# set python env
venv = run([POETRY_BIN,"env","info","--path"],
    text=True,capture_output=True).stdout.strip()

if venv == "":
    raise Exception("Error, no python env found")

# set SWeetheart Shell command -> sws
with open(f"{SWS_PATH}/sws","w") as file_out:
    file_out.write(f"""

#!/bin/sh
#NOTE: faster than 'poetry run' to start
{venv}/bin/python3 -m sweetheart.sweet shell '$*'

    """.strip())

os.chmod(f"{SWS_PATH}/sws",stat.S_IRWXU|stat.S_IRGRP|stat.S_IROTH)
print("\n")

if not SWS_PATH in os.environ['PATH']:
    run(['echo',f"export $PATH={SWS_PATH}:$PATH",'>>','~/.bashrc'])
    print(f"{SWS_PATH} added to $PATH")

# exit message
print("all done installing sweetheart\n",
    "type 'sws --help' for getting some help\n")
