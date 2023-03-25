"""
provide installation tools for getting
sweetheart requirements and resources
"""
import os,sys,json,stat
import subprocess as sp

HOME = os.environ['HOME']
PATH = os.environ['PATH']


# ensure prerequisites for sweetheart
# this installs poetry and sws with minimum capabilities
if not os.path.isfile(
    f"{HOME}/.sweet/sweetheart/programs/my_python/pyproject.toml" ):

    # provide which as python func
    wh = lambda command: sp.run(
        f"which {command}",
        shell=True,text=True,capture_output=True,
        ).stdout.strip()

    sws_script = f"{HOME}/.local/bin/sws"
    poetry = wh('poetry') or wh('~/.local/bin/poetry')
    sp_conf_file = f"{HOME}/.sweet/sweetheart/configuration/subproc.json"

    if not poetry:
        assert wh('curl') and wh('python3')
        sp.run("curl -sSL https://install.python-poetry.org|python3 -",shell=True)
        poetry = wh('poetry') or wh('~/.local/bin/poetry')
        assert poetry

    # make required directories
    os.makedirs(f"{HOME}/.sweet/sweetheart/programs",exist_ok=True)
    os.makedirs(f"{HOME}/.sweet/sweetheart/configuration",exist_ok=True)
    
    # build my_python directory
    os.chdir(f"{HOME}/.sweet/sweetheart/programs/my_python")
    sp.run(f"{poetry} init -n",shell=True)

    if "--github" in sys.argv:
        # install sweetheart from github repository
        src = "https://github.com/IncredibleProgress/sweetheart.py.git"
        sp.run(f"{poetry} add git+{src}",shell=True)
    else:
        # install sweetheart from pypi repository
        sp.run(f"{poetry} add sweetheart",shell=True)

    # set python env
    venv = sp.run(
        f"{poetry} env info --path",
        shell=True,text=True,capture_output=True,
        ).stdout.strip()

    # provide subroc.conf file
    if venv=="": raise Exception("!Error, no Python env found")
    with open(sp_conf_file,"w") as file_out:
        json.dump({ 'pyenv': venv },file_out)

    # provide sws command (faster than 'poetry run')
    with open(sws_script,"w") as file_out:
        file_out.write(f"#!/bin/sh\n{venv}/bin/python3 -m sweetheart.cli sh $*")
    
    # authorize execution of sws
    os.chmod(sws_script,stat.S_IRWXU|stat.S_IRGRP|stat.S_IROTH)

    if f"{HOME}/.local/bin" not in PATH:
        # export ~/.local/bin within .bashrc
        with open("{HOME}/.bashrc","a") as file_out:
            file_out.write(f"\nexport PATH={HOME}/.local/bin:$PATH")


if __name__ == "__main__": 

    if "--init" in sys.argv:
        # autostart init process for full install
        sp.run("bash sws --init",shell=True)

    # STOP install module execution here
    # a sweetheart config is required for next utilities
    exit()


  #############################################################################
 ## Sweetheart Install Tools #################################################
#############################################################################

from sweetheart import *
#NOTE: sp is replaced here by sp class of sweetheart

from zipfile import ZipFile
from urllib.parse import urljoin
from urllib.request import urlretrieve

master_pyproject = f"{BaseConfig.HOME}/.sweet/{MASTER_MODULE}/programs/my_python/pyproject.toml"
raw_github = "https://raw.githubusercontent.com/IncredibleProgress/sweetheart.py/master/get-sweetheart.py"

def init(config:BaseConfig,add_pylibs=""):
    """ set require minimal features for working with sweetheart """

    # set python env with basic project settings
    if config.project != MASTER_MODULE:
        sp.init_project_env(config.project)

    if config.project.startswith("jupyter"):
        echo("INFO: init jupyter as a specific project")
        return

    # required directories
    for basedir in [
          #f"{config.root_path}/configuration",
          f"{config.root_path}/database",
          f"{config.root_path}/documentation/notebooks",
          #f"{config.root_path}/programs/scripts",
          f"{config.root_path}/webpages/templates",
          f"{config.root_path}/webpages/resources" ]:
        os.makedirs(basedir,exist_ok=True)

    PKG_INIT = {
        # set minimum distro resources
        'aptlibs': ["*unit","*rethinkdb","*nodejs","cargo"],
        'dnflibs': [],#FIXME: rhel not yet implemented
        # set minimum rust resources
        'cargolibs': ["cargo-binstall"],
        'cargobin': ["mdbook"],
        # set minimum js and python resources        
        'npmlibs': ["brython","tailwindcss","daisyui","vue@latest"],# Vue3
        'pylibs': ["rethinkdb","starlette"],
        # set documentation and further resources
        'files': [
            # set the documentation .zip package
            "documentation/sweetbook.zip",
            # set the other needed files
            "configuration/packages.json",
            "webpages/HTML",
            "webpages/resources/favicon.ico",
            "webpages/resources/tailwind.base.css",
            "webpages/resources/tailwind.config.js" ]}
    
    if config.project != MASTER_MODULE:
        # unset libs installation
        del PKG_INIT['aptlibs'],PKG_INIT['dnflibs']
        #del PKG_INIT['cargolibs']

    if "fastapi" in add_pylibs:
        # avoid versions conflict with starlette
        PKG_INIT['pylibs'].remove("starlette")

    if "jupyter" in add_pylibs:
        # set ipykernel instead of jupyter
        # this allow runing python env within VS Code
        PKG_INIT['pylibs'].remove("jupyter")
        PKG_INIT['pylibs'].append("ipykernel")

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
        from sweetheart.heart import JupyterLab
        JupyterLab(config).set_ipykernel(set_pwd=False)
   
    try:
        # provide sweetheart html documentation    
        os.symlink(f"{config.root_path}/documentation/sweetbook/book",
            f"{config.root_path}/webpages/sweetbook")
        # # provide installed javascript libs within Ubuntu/Debian
        # os.symlink("/usr/share/javascript",
        #     f"{config.root_path}/webpages/resources/javascript")
    except:
        verbose("INFO:\n an error occurred creating symlinks during init process",
            "\n an expected cause could be that links are already existing")
    
    echo("installation process completed",blank=True)

    
class BaseInstall:

    def __init__(self,config:BaseConfig):

        assert sp.is_executable('npm')
        assert sp.is_executable('cargo')

        self.config = config
        self.packages_file = f"{config.root_path}/configuration/packages.json"
        
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
        return sp.run("sudo","apt","install",*libs,**kwargs)

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
        return sp.run("sudo","dnf","install",*libs,**kwargs)

    def cargo(self,*libs:str,**kwargs):
        """ install rust crates using cargo """

        echo("cargo install:",*libs,blank=True)
        return sp.run(f"cargo","install",*libs,**kwargs)
    
    def poetry(self,*libs:str,**kwargs):
        """ install python packages using poetry """

        echo("poetry add:",*libs,blank=True)
        return sp.poetry("add",*libs,**kwargs)

    def npm(self,*libs:str,init=False,**kwargs):
        """ install node modules using npm """

        echo("npm install:",*libs,blank=True)
        os.chdir(f"{self.config.root_path}/webpages/resources")
        if init: sp.run("npm","init","--yes")
        return sp.run("npm","install",*libs,**kwargs)

    def install_libs(self,libs:dict,init:bool=False):
        """ install given libs using apt,cargo,poetry,npm
            and download listed files from github if given
            no libs arg will set init process for new project """

        aptlibs = libs.get('aptlibs')
        if "debian" in distbase and aptlibs:
            self.apt(*aptlibs)

        dnflibs = libs.get('dnflibs')
        if "rhel" in distbase and dnflibs:
            self.dnf(*dnflibs)

        cargolibs = libs.get('cargolibs')
        if cargolibs: self.cargo(*cargolibs)

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
            if pth.startswith("documentation") and path.endswith(".zip"):
                self.unzip_doc(file)

    def unzip_doc(self,zipfile:str,remove:bool=True):
        """ unzip and build documentation 
            this require using the mdbook rust crate"""

        os.chdir(f"{self.config.root_path}/documentation")
        name,ext = os.path.splitext(zipfile)
        assert ext == ".zip"

        with ZipFile(zipfile,"r") as zf: zf.extractall()
        sp.shell(f"{self.config.rust_crates}/mdbook build {name}")
        if remove: os.remove(zipfile)

    def install_packages(self,*packages:str):
        """ install selected sweetheart packages """

        with open(self.packages_file) as fi:
            json_pkg = json.load(fi)

        for pkg in packages:
            self.install_libs(json_pkg[pkg])


    def apt_install_nodejs(self):
        """ install nodejs and npm on debian/ubuntu systems """

        ver = self.config.node_version
        exe = sp.list_executables("node npm")

        # set official repository and install nodejs
        if "node" not in exe and "npm" not in exe:
            verbose(f"set NodeJS {ver} LTS repository from nodesource.com")
            sp.shell(f"curl -fsSL https://deb.nodesource.com/setup_{ver} | sudo -E bash - && apt-get install -y nodejs")


    def apt_install_unit(self):
        """ install Nginx Unit on debian/ubuntu systems 
            will set official Nginx repository if needed """

        #NOTE: works with current behavior of poetry
        assert self.config.python_env.endswith(self.config.python_version)

        if not sp.stdout("apt policy unit"):
            # set official Nginx Unit repository
            sp.read_sh(f"""
echo "set Nginx Unit repository from nginx.org"
echo "deb https://packages.nginx.org/unit/{sp.distrib}/ {sp.codename} unit" | sudo tee /etc/apt/sources.list.d/unit.list
wget -qO- https://unit.nginx.org/keys/nginx-keyring.gpg | sudo apt-key add - 
            """.strip() )

        if not sp.is_executable("unitd"):
            # install Nginx Unit packages
            version = self.config.python_version
            sp.shell("sudo apt update")
            sp.shell(f"sudo apt install unit unit-python{version}") 


    def apt_install_rethinkdb(self):
        """ install rethinkdb on debian/ubuntu systems
            will set official RethinkDB repository if needed """

        if not sp.stdout("apt policy rethinkdb"):
            # set offical RethinkDB repository
            sp.read_sh(f"""
echo "set RethinkDB repository from rethinkdb.com"
echo "deb https://download.rethinkdb.com/repository/{sp.distrib}-{sp.codename} {sp.codename} main" | sudo tee /etc/apt/sources.list.d/rethinkdb.list
wget -qO- https://download.rethinkdb.com/repository/raw/pubkey.gpg | sudo apt-key add -
            """.strip() )

        if not sp.executable("rethinkdb"):
            # install rethinkdb package
            sp.shell("sudo apt update")
            sp.shell(f"sudo apt install rethinkdb")
