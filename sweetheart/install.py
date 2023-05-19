"""
install.py
install the sweetheart requirements and resources

available command line options:
    --github   get sweetheart from github instead of pypi
    --init     autostart the initialization process 

#FIXME: rust crates sourcing
    install.py implements 2 diffrent ways for installing rust crates
    one using cargo and one using cargo-binstall (currently for tests)
"""

import subprocess
import os,sys,json,stat

from zipfile import ZipFile
from urllib.parse import urljoin as __urljoin
from urllib.request import urlopen,urlretrieve

def urljoin(base:str,*args,**kwargs) -> str:
    # avoid unexpected behavior with urljoin
    if not base.endswith('/'): base+='/'
    return __urljoin(base,*args,**kwargs)

def urlget(url:str) -> bytes:
    with urlopen(url) as file_like_object:
        #FIXME: should return bytes in most cases
        return file_like_object.read()


HOME = os.environ['HOME']
PATH = os.environ['PATH']
raw_github = "https://raw.githubusercontent.com/IncredibleProgress/sweetheart.py/master/"

# ensure prerequisites for sweetheart
# this installs poetry and sws with minimum capabilities
if not os.path.isfile(
    f"{HOME}/.sweet/sweetheart/programs/my_python/pyproject.toml" ):

    # provide which as python func
    which = lambda command: subprocess.run(
        ["which",command],
        text=True,capture_output=True,
        ).stdout.strip()

    sws_script = f"{HOME}/.local/bin/sws"
    poetry = which('poetry') or which('~/.local/bin/poetry')
    sp_conf_file = f"{HOME}/.sweet/sweetheart/configuration/subproc.json"

    if not poetry:
        python3 = which('python3')
        subprocess.run([python3],input=urlget("https://install.python-poetry.org"))
        poetry = which('poetry') or which('~/.local/bin/poetry')
        assert poetry

    # make required directories
    os.makedirs(f"{HOME}/.sweet/sweetheart/programs/my_python",exist_ok=True)
    os.makedirs(f"{HOME}/.sweet/sweetheart/configuration",exist_ok=True)

    # build my_python directory
    os.chdir(f"{HOME}/.sweet/sweetheart/programs/my_python")
    subprocess.run([poetry,"init","-n"])

    if "--github" in sys.argv:
        # install sweetheart from github repository
        src = "https://github.com/IncredibleProgress/sweetheart.py.git"
        subprocess.run([poetry,"add",f"git+{src}"])
    else:
        # install sweetheart from pypi repository
        subprocess.run([poetry,"add","sweetheart"])

    # set python env
    venv = subprocess.run(
        [poetry,"env","info","--path"],
        text=True,capture_output=True,
        ).stdout.strip()

    # provide subroc.conf file
    if venv=="": raise Exception("!Error, no Python env found")
    with open(sp_conf_file,"w") as file_out:
        json.dump({ 'pyenv': venv },file_out)

    # provide sws command (faster than 'poetry run')
    with open(sws_script,"w") as file_out:
        file_out.write(f"#!/bin/sh\n{venv}/bin/python3 -m sweetheart.cli $*")
    
    # authorize execution of sws
    os.chmod(sws_script,stat.S_IRWXU|stat.S_IRGRP|stat.S_IROTH)

    if f"{HOME}/.local/bin" not in PATH:
        # export ~/.local/bin within .bashrc
        with open(f"{HOME}/.bashrc","a") as file_out:
            file_out.write(f"\nexport PATH={HOME}/.local/bin:$PATH")


if __name__ == "__main__": 

    if "--init" in sys.argv:
        # autostart init process for full install
        subprocess.run(["bash","-c","sws init"])

    # STOP install.py module execution here
    # a sweetheart config is required for using next utilities
    exit()


  #############################################################################
 ## Sweetheart Installation Tools ############################################
#############################################################################

del os,stat,subprocess
from sweetheart import *


def init_project_env(project_name:str):
    """ create and init new python env for new project 
        install *ipykernel* for basic jupyter features """

    assert project_name != MASTER_MODULE

    _path = f"{BaseConfig.HOME}/.sweet/{project_name}"
    _my_python = f"{_path}/programs/my_python"

    os.makedirs(f"{_path}/documentation/notebooks",exist_ok=True)
    os.makedirs(f"{_path}/configuration",exist_ok=True)
    os.makedirs(_my_python,exist_ok=True)

    # init a new python env with *ipykernel* for new project 
    sp.poetry("init","-n",cwd=_my_python)
    sp.poetry("add","ipykernel",cwd=_my_python)
    pyenv = sp.set_python_env(cwd=_my_python)

    with open(f"{_path}/configuration/subproc.json","w") as fi:
        json.dump({ 'pyenv': pyenv },fi)


def init(config:BaseConfig,add_pylibs="",no_pkg_init=False):
    """ set require minimal features for working with sweetheart """

    # set python env with basic project settings
    if config.project != MASTER_MODULE:
        init_project_env(config.project)

    if config.project.startswith("jupyter"):
        #TODO: lead jupyter/jupyterlab/jupyterhub matter
        echo("init a jupyter specific project for running jupyter",blank=True)

        config = set_config(project="jupyter")
        sp.poetry("add","jupyterlab")

        from sweetheart.services import JupyterLab
        jpy = JupyterLab(config)
        jpy.set_ipykernel(set_passwd=True)
        jpy.set_service("[SWEETHEART] JupyterLab server")
        jpy.enable_service("jupyterlab.service")

    if no_pkg_init or config.project.startswith("jupyter"):
        # stop init process here
        return

    # required extra directories
    os.makedirs(f"{config.root_path}/database",exist_ok=True)
    os.makedirs(f"{config.root_path}/webpages/templates",exist_ok=True)
    os.makedirs(f"{config.root_path}/webpages/resources",exist_ok=True)
    os.makedirs(f"{config.root_path}/documentation/notebooks",exist_ok=True)

    PKG_INIT = {
        # set minimum distro resources
        'aptlibs': ["*unit","*rethinkdb","*nodejs","cargo"],
        'dnflibs': [],#TODO: rhel not yet implemented
        # set minimum rust resources
        'cargolibs': ["cargo-binstall"],
        'cargobin': ["mdbook"],
        # set minimum js and python resources
        # ipykernel allows working with jupyter e.g. within VS-Code      
        'npmlibs': ["brython","tailwindcss","vue@latest"],# Vue3
        'pylibs': ["rethinkdb","starlette","ipykernel"],
        # set documentation and further resources
        'files': [
            # set the documentation .zip package
            "documentation/sweetdoc.zip",
            # set the other needed files
            "configuration/packages.json",
            "webpages/templates/HTML_BASE",
            "webpages/resources/favicon.ico",
            #"webpages/resources/sweetheart.js",
            "webpages/resources/tailwind.base.css",
            "webpages/resources/tailwind.config.js" ]}

    if config.project != MASTER_MODULE:
        # unset global libs installation
        del PKG_INIT['aptlibs'], PKG_INIT['dnflibs']
        del PKG_INIT['cargolibs'], PKG_INIT['cargobin']

    if "fastapi" in add_pylibs:
        # avoid version conflict with starlette
        PKG_INIT['pylibs'].remove("starlette")

    # if "jupyter" in add_pylibs:
    #     # avoid version conflict with ipykernel
    #     PKG_INIT['pylibs'].remove("ipykernel")

    # set given python extra modules
    if isinstance(add_pylibs,list):
        PKG_INIT['pylibs'].extend(add_pylibs)
    elif isinstance(add_pylibs,str):
        PKG_INIT['pylibs'].extend(add_pylibs.split())

    # install default libs with extra modules
    installer = BaseInstall(config)
    installer.install_libs(PKG_INIT,init=True)
    
    # build default tailwind.css file
    sp.shell(config.subproc['.tailwindcss'],\
        cwd=f"{config.root_path}/webpages/resources")

    if "ipykernel" in PKG_INIT['pylibs']:
        # set python env into jupyter
        from sweetheart.services import JupyterLab
        JupyterLab(config).set_ipykernel(set_passwd=False)
   
    try:
        # provide sweetheart html documentation within webpages
        os.symlink(f"{config.root_path}/documentation/sweetdoc/book",
            f"{config.root_path}/webpages/sweetdoc")
    except:
        verbose("WARN: symlink to sweetdoc already existing ?")
    
    echo("installation process completed",blank=True)


class BaseInstall:

    def __init__(self,config:BaseConfig):

        self.config = self._ = config
        self.packages_file = f"{config.root_path}/configuration/packages.json"
    
    @sudo
    def apt(self,*libs:str,**kwargs):
        """ install distro packages using 'apt install'
            this leads specific treatments for given *libs 
            dedicated for debian/ubuntu distros branch """

        libs = list(libs)
        echo("apt install:",*libs,blank=True)

        # specific treatments for subprocesses
        if "*nodejs" in libs:
            self.apt_install_nodejs()
            libs.remove("*nodejs")

        if "*rethinkdb" in libs:
            self.apt_install_rethinkdb()
            libs.remove("*rethinkdb")

        if "*unit" in libs:
            self.apt_install_unit()
            libs.remove("*unit")

        # install other packages
        # NOTE: sp.sudo() couldn't work porperly here
        return sp.shell("sudo","-S","apt-get","install","-y",*libs,**kwargs)

    @sudo
    def dnf(self,*libs:str,**kwargs):
        """ FIXME: coming soon !
            install distro packages using 'dnf install'
            this leads specific treatments for given *libs 
            dedicated for rhel/almalinux distros branch """

        # specific treatments for subprocesses
        if "*rethinkdb" in libs:
            raise NotImplementedError
            libs.remove("*rethinkdb")

        if "*unit" in libs:
            raise NotImplementedError
            libs.remove("*unit")

        # install other packages
        return sp.sudo("dnf","install",*libs,**kwargs)

    def cargo(self,*libs:str,bin:bool=False,**kwargs):
        """ install rust crates (given libs) using cargo 
            will use cargo-binstall when bin is set at True """

        if bin == False:
            echo("cargo install:",*libs,blank=True)
            return sp.shell(f"cargo","install",*libs,**kwargs)

        elif bin == True:
            echo("cargo-binstall:",*libs,blank=True)
            binstall = f"{self.config.rust_crates}/cargo-binstall"
            return sp.shell(binstall,*libs,**kwargs)

        else: raise TypeError
    
    def poetry(self,*libs:str,**kwargs):
        """ install python packages using poetry """

        echo("poetry add:",*libs,blank=True)
        return sp.poetry("add",*libs,**kwargs)

    def npm(self,*libs:str,init=False,**kwargs):
        """ install node modules using npm """

        echo("npm install:",*libs,blank=True)
        os.chdir(f"{self.config.root_path}/webpages/resources")
        if init: sp.shell("npm","init","--yes")
        return sp.shell("npm","install",*libs,**kwargs)

    def install_libs(self,libs:dict,init:bool=False):
        """ install given libs using apt,cargo,poetry,npm
            and download listed files from github if given
            no libs arg will set init process for new project """

        aptlibs = libs.get('aptlibs')
        if "debian" in os.distbase and aptlibs:
            self.apt(*aptlibs)

        dnflibs = libs.get('dnflibs')
        if "rhel" in os.distbase and dnflibs:
            self.dnf(*dnflibs)

        cargolibs = libs.get('cargolibs')
        if cargolibs: self.cargo(*cargolibs)

        # cargo-binstall must be installed 
        cargobin = libs.get('cargobin')
        if cargobin: self.cargo(*cargobin,bin=True)

        npmlibs = libs.get('npmlibs')
        if npmlibs: self.npm(*npmlibs,init=init)

        pylibs = libs.get('pylibs')
        if pylibs: self.poetry(*pylibs)

        files = libs.get('files')
        if files: self.download(*files)

    def download(self,*files_list:str):
        """ download given listed files from github 
            unzip documentation when given within files """

        for relpath in files_list:

            # download files at the given path
            echo("download file:",relpath)
            urlretrieve(urljoin(raw_github,relpath),
                os.path.join(self.config.root_path,relpath))

            # unzip doc when given
            pth,file = os.path.split(relpath)
            if pth.startswith("documentation") and file.endswith(".zip"):
                self.unzip_doc(file)

    def unzip_doc(self,zipfile:str,remove:bool=True):
        """ unzip and build documentation 
            this require using the mdbook rust crate"""

        os.chdir(f"{self.config.root_path}/documentation")
        name,ext = os.path.splitext(zipfile)
        assert ext == ".zip"

        with ZipFile(zipfile,"r") as zf: zf.extractall()
        sp.shell(f"{self.config.rust_crates}/mdbook","build",name)
        if remove: os.remove(zipfile)

    def install_packages(self,*packages:str):
        """ install selected sweetheart packages """

        with open(self.packages_file) as fi:
            json_pkg = json.load(fi)

        for pkg in packages:
            self.install_libs(json_pkg[pkg])

    @sudo
    def apt_install_nodejs(self):
        """ install nodejs and npm on debian/ubuntu systems """

        ver = self.config.node_version
        exe = sp.list_executables("node npm")

        if "node" not in exe and "npm" not in exe:
            # set official repository and install nodejs
            script = urlget(f"https://deb.nodesource.com/setup_{ver}")
            verbose(f"set NodeJS {ver} LTS repository from nodesource.com")

            assert isinstance(script,bytes)
            sp.shell("sudo","-E","bash",input=script,stdout=os.DEVNULL)
            sp.shell("sudo","apt-get","install","-y","nodejs")

    @sudo
    def apt_install_unit(self):
        """ install Nginx Unit on debian/ubuntu systems 
            will set official Nginx repository if needed """

        #NOTE: works with current behavior of poetry
        assert self.config.python_env.endswith(self.config.python_version)

        if not sp.stdout("apt policy unit"):

            echo("set Nginx Unit repository from nginx.org")
            key = urlget("https://unit.nginx.org/keys/nginx-keyring.gpg")

            sp.shell("sudo","tee","/etc/apt/sources.list.d/unit.list",text=True,
                input=f"deb https://packages.nginx.org/unit/{os.distrib}/ {os.codename} unit")

            assert isinstance(key,bytes)
            sp.shell("sudo","apt-key","add",input=key,stdout=os.DEVNULL)

        if not sp.is_executable("unitd"):
            # install Nginx Unit packages
            version = self.config.python_version
            sp.sudo("apt-get","update",stdout=os.DEVNULL)
            sp.sudo("apt-get","install","-y","unit",f"unit-python{version}") 

    @sudo
    def apt_install_rethinkdb(self):
        """ install rethinkdb on debian/ubuntu systems
            will set official RethinkDB repository if needed """

        if not sp.stdout("apt policy rethinkdb"):

            echo("set RethinkDB repository from rethinkdb.com")
            key = urlget("https://download.rethinkdb.com/repository/raw/pubkey.gpg")

            sp.shell("sudo","tee","/etc/apt/sources.list.d/rethinkdb.list",text=True,
                input=f"deb https://download.rethinkdb.com/repository/{os.distrib}-{os.codename} {os.codename} main")

            assert isinstance(key,bytes)
            sp.shell("sudo","apt-key","add",input=key,stdout=os.DEVNULL)

        if not sp.is_executable("rethinkdb"):
            # install rethinkdb package
            sp.sudo("apt-get","update",stdout=os.DEVNULL)
            sp.sudo("apt-get","install","-y","rethinkdb")
