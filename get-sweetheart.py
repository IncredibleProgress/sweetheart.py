"""
get-sweetheart.py: the github sweetheart installer
allow installation without any python dependencies matter
"""
import os,stat
from subprocess import run

poetry_bin = f"{os.environ['HOME']}/.poetry/bin/poetry"
sweet_path = f"{os.environ['HOME']}/.sweet/sweetheart/programs"
sws_path = f"{os.environ['HOME']}/.sweet/sweetheart/programs/scripts/sws"

if not os.path.isfile(poetry_bin):

    curl = "curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -"
    run(curl,shell=True)

os.makedirs(sweet_path,exist_ok=True)
os.makedirs(os.path.split(sws_path)[0],exist_ok=True)

os.chdir(sweet_path)
run([poetry_bin,"new","my_python"])

os.chdir("my_python")
run([poetry_bin,"add","sweetheart"])

venv = run([poetry_bin,"env","info","--path"],
    text=True,capture_output=True).stdout.strip()

assert venv
with open(sws_path,"w") as file_out:
    file_out.write(f"""

#!/bin/bash
#NOTE: much faster than poetry for starting
{venv}/bin/python3 -m sweetheart.sweet $*

    """.strip())

os.chmod(sws_path,stat.S_IRWXU|stat.S_IRWXG|stat.S_IRWXO)
print("\nall done\n")
