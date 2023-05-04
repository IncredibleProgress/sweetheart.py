
import os as _os_
import shlex as _shlex_
import tempfile as _tempfile_
import subprocess as _subprocess_
import platform,getpass,locale,shutil


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

    # tempfiles utilities
    TemporaryFile = _tempfile_.TemporaryFile
    SpooledTemporaryFile = _tempfile_.SpooledTemporaryFile

    # shell features
    which = shutil.which
    DEVNULL = _subprocess_.DEVNULL

    @staticmethod
    def run(*args,**kwargs):
        """
        hardened subprocess.run 
        protect against shell injection
        """
        if kwargs.get('shell'):
            raise Exception("running shell is not allowed")
        else:
            assert len(args) == 1
            return _subprocess_.run(*args,**kwargs)

    @staticmethod
    def shell(*args,**kwargs):
        """ 
        run given args as a command providing some flexibility with args
        it will accept simple shell-like commands/args separated by spaces
        but THIS IS NOT shell and usual shell features are not available
        it uses os.run() behind and shell=True is not allowed within for security reason 
        meaning that in any case it won't never pass through the real shell subprocess
        instead the args given with os.run() are directly committed to the linux kernel
        """

        if len(args)==1 and isinstance(args[0],str):
            # split given str but doesn't pass shell=True
            return os.run(_shlex_.split(args[0]),**kwargs)

        elif len(args)==1 and isinstance(args[0],list):
            return os.run(args[0],**kwargs)
        
        else: 
            # zip the args into a list given as first arg to run()
            # allow shell("echo","hello") rather than shell(["echo","hello"])
            return os.run(args,**kwargs)

    # provide a direct way for getting the stdout
    stdout = lambda *args,**kwargs:\
        sp.shell(*args,text=True,capture_output=True,**kwargs).stdout.strip()
            