
import os as _os
import platform,getpass,locale,subprocess,shutil

class os:

    """ reimplements common tools of the python os module 
        but extended with some foreign facilities for ease """

    env = environ = _os.environ
    getenv = _os.getenv
    putenv = _os.putenv

    getcwd = _os.getcwd
    getuser = getpass.getuser()
    get_exec_path = _os.get_exec_path
    getlocale = locale.getlocale

    path = _os.path
    isdir = _os.path.isdir
    isfile = _os.path.isfile
    islink = _os.path.islink
    expanduser = _os.path.expanduser

    chdir = _os.chdir
    mkdir = _os.mkdir
    makedirs = _os.makedirs
    symlink = _os.symlink
    remove = _os.remove
    rmtree = shutil.rmtree
    listdir = _os.listdir
    walk = _os.walk

    # provide distro infos
    os_release = platform.freedesktop_os_release()
    distrib = os_release['ID'].lower()
    distbase = os_release['ID_LIKE'].lower()
    codename = os_release['UBUNTU_CODENAME'].lower()

    # shell features
    run = subprocess.run
    which = shutil.which

    # get os_release with Python <= 3.9 :
    # 
    #     import csv
    #     os_release = {}
    #     with open("/etc/os-release") as fi:
    #          reader = csv.reader(fi,delimiter="=")
    #          for line in reader:
    #             if line==[]: continue # this can happen...
    #             os_release[line[0]] = line[1]
    #

    @staticmethod
    def enforced_symlink(source,dest):

        if os.path.islink(dest): print(f"Warning, existing link {dest}")
        elif os.path.isfile(dest): os.remove(dest)
        elif os.path.isdir(dest) : shutil.rmtree(dest)
        try: os.symlink(source,dest)
        except: pass
