
import sys
from sweetheart.globals import *

from zipfile import ZipFile
from urllib.parse import urljoin
from urllib.request import urlretrieve

distrib = sp.os_release['ID'].lower()
distbase = sp.os_release['ID_LIKE'].lower()
codename = sp.os_release['UBUNTU_CODENAME'].lower()

master_pyproject = f"{BaseConfig.HOME}/.sweet/{MASTER_MODULE}/programs/my_python/pyproject.toml"
raw_github = "https://raw.githubusercontent.com/IncredibleProgress/sweetheart.py/master/get-sweetheart.py"

# ensure prerequisites
if not os.path.isfile(master_pyproject):
    sp.shell(f"curl -sSL {raw_github} | python3 -")


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
          #f"{config.root_path}/documentation/notebooks",
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
            # set documentation .zip package
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
            print(f"set NodeJS {ver} LTS repository from nodesource.com")
            sp.shell(f"curl -fsSL https://deb.nodesource.com/setup_{ver} | sudo -E bash - && apt-get install -y nodejs")


    def apt_install_unit(self):
        """ install Nginx Unit on debian/ubuntu systems 
            will set official Nginx repository if needed """

        _ = self.config
        #NOTE: works with current behavior of poetry
        assert _.python_env.endswith(_.python_version)

        script = f"""
echo "set Nginx Unit repository from nginx.org"
echo "deb https://packages.nginx.org/unit/{distrib}/ {codename} unit" | sudo tee /etc/apt/sources.list.d/unit.list
wget -qO- https://unit.nginx.org/keys/nginx-keyring.gpg | sudo apt-key add - """

        # set official Nginx Unit repository
        if not sp.stdout("apt policy unit"):
            sp.read_sh(script)
            sp.shell("sudo apt update")

        # install Nginx Unit packages
        if not sp.is_executable("unitd"):
            version = self.config.python_version
            sp.shell(f"sudo apt install unit unit-python{version}") 


    def apt_install_rethinkdb(self):
        """ install rethinkdb on debian/ubuntu systems
            will set official RethinkDB repository if needed """

        _ = self.config; script = f"""
echo "set RethinkDB repository from rethinkdb.com"
echo "deb https://download.rethinkdb.com/repository/{distrib}-{codename} {codename} main" | sudo tee /etc/apt/sources.list.d/rethinkdb.list
wget -qO- https://download.rethinkdb.com/repository/raw/pubkey.gpg | sudo apt-key add - """

        # set offical RethinkDB repository
        if not sp.stdout("apt policy rethinkdb"):
            sp.read_sh(script)
            sp.shell("sudo apt update")

        # update Rethinkdb package
        if not sp.is_executable("rethinkdb"):
            sp.shell(f"sudo apt install rethinkdb")

