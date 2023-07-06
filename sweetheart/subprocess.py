
import platform,locale,shutil

import os as _os_
import shlex as _shlex_
import getpass as _getpass_
import tempfile as _tempfile_
import subprocess as _subprocess_
import multiprocessing as _multiprocessing_


class os:

    """ reimplements common tools of the python os module
        and extends it with some foreign facilities for ease 
        it intends to ensure best practices using standard libs """

    env = environ = _os_.environ
    getenv = _os_.getenv
    putenv = _os_.putenv

    getcwd = _os_.getcwd
    getuser = _getpass_.getuser
    getpass = _getpass_.getpass
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
    codename = os_release.get('UBUNTU_CODENAME').lower()

    # tempfiles utilities
    TemporaryFile = _tempfile_.TemporaryFile
    SpooledTemporaryFile = _tempfile_.SpooledTemporaryFile

    # multiprocessing features
    Process = _multiprocessing_.Process

    # shell-like features
    which = shutil.which
    DEVNULL = _subprocess_.DEVNULL

    @staticmethod
    def run(*args,**kwargs):
        """ securized subprocess.run() function with shell=True forbidden
            this intends to protect code against shell injection attacks """

        if kwargs.get('shell'):
            raise Exception("running shell is not allowed")
        else:
            assert len(args)==1
            return _subprocess_.run(*args,**kwargs)

    @staticmethod
    def shell(*args,**kwargs):
        """ 
        it will run given args as a command providing some flexibility with args 
        accepts simple shell-like commands and args separated by spaces in a string
        THIS IS NOT shell and usual shell or bash features are not available here
        """

        if len(args)==1 and isinstance(args[0],str):
            # split given str but doesn't pass shell=True
            #NOTE: for security sudo should not be used here
            args = _shlex_.split(args[0])
            assert "sudo" not in args[0]
            return os.run(args,**kwargs)

        elif len(args)==1 and isinstance(args[0],list):
            return os.run(args[0],**kwargs)
        
        else: 
            # zip the args into a list given as first arg to run()
            # allow shell("echo","hello") rather than shell(["echo","hello"])
            return os.run(args,**kwargs)

    @staticmethod
    def stdout(*args,**kwargs):
        """ provide a direct way for getting the stdout """
        
        assert 'text' not in kwargs
        assert 'capture_output' not in kwargs

        return os.shell(
            *args,
            text=True,
            capture_output=True,
            **kwargs).stdout.strip()
