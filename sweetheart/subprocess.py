
import os as _os_
import platform,getpass,locale,subprocess,shutil


class os:

    """ reimplements common tools of the python os module 
        and extends it with some foreign facilities for ease """

    env = environ = _os_.environ
    getenv = _os_.getenv
    putenv = _os_.putenv

    getcwd = _os_.getcwd
    getuser = getpass.getuser
    getpass = getpass.getpass
    get_exec_path = _os_.get_exec_path
    getlocale = locale.getlocale

    path = _os_.path
    isdir = _os_.path.isdir
    isfile = _os_.path.isfile
    islink = _os_.path.islink
    expanduser = _os_.path.expanduser

    chdir = _os_.chdir
    mkdir = _os_.mkdir
    makedirs = _os_.makedirs
    symlink = _os_.symlink
    remove = _os_.remove
    rmtree = shutil.rmtree
    listdir = _os_.listdir
    #walk = _os_.walk

    # provide distro infos
    os_release = platform.freedesktop_os_release()
    distrib = os_release['ID'].lower()
    distbase = os_release['ID_LIKE'].lower()
    codename = os_release['UBUNTU_CODENAME'].lower()

    # shell features
    run = subprocess.run
    which = shutil.which
    DEVNULL = subprocess.DEVNULL

    @staticmethod
    def enforced_symlink(source,dest):

        if os.path.islink(dest): print(f"Warning, existing link {dest}")
        elif os.path.isfile(dest): os.remove(dest)
        elif os.path.isdir(dest) : shutil.rmtree(dest)
        try: os.symlink(source,dest)
        except: pass

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