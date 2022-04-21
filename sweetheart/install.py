
from sweetheart.globals import *

from zipfile import ZipFile
from urllib.parse import urljoin
from urllib.request import urlretrieve

master_pyproject = f"{BaseConfig.HOME}/.sweet/{MASTER_MODULE}/programs/my_python/pyproject.toml"
raw_github = "https://raw.githubusercontent.com/IncredibleProgress/sweetheart.py/master/"# / is needed

# ensure prerequisites
if not os.path.isfile(master_pyproject):
    sp.shell(f"curl -sSL {raw_github}get-sweetheart.py | python3 - --rethinkdb")


def init(config:BaseConfig,add_pylibs:str=""):
    """ set require minimal features for working with sweetheart """

    PKG_INIT = {
        'cargolibs': ["mdbook"],
        'aptlibs': ["xterm","rustc","rethinkdb","nodejs"],
        'npmlibs': ["brython","tailwindcss","vue@next"],# Vue3
        'pylibs': ["rethinkdb","uvicorn[standard]","aiofiles","starlette"],# starlette at end

        'files': ["documentation/sweetbook.zip","configuration/packages.json","webpages/HTML",
            "webpages/resources/tailwind.base.css","webpages/resources/tailwind.config.js",
            "webpages/resources/favicon.ico"],'documentation': "sweetbook.zip" }

    #FIXME: starlette version matter installing fastapi 
    if "fastapi" in add_pylibs: del PKG_INIT['pylibs'][-1]

    # require directories
    for basedir in [
        f"{config.root_path}/configuration",
        f"{config.root_path}/database",
        f"{config.root_path}/documentation/notebooks",
        f"{config.root_path}/programs/scripts",
        f"{config.root_path}/webpages/templates",
        f"{config.root_path}/webpages/resources",
    ]: os.makedirs(basedir,exist_ok=True)

    # install default libs with given extra modules
    if isinstance(add_pylibs,list):
        PKG_INIT['pylibs'].extend(add_pylibs)
    elif isinstance(add_pylibs,str):
        PKG_INIT['pylibs'].extend(add_pylibs.split())

    installer = BaseInstall(config)
    installer.install_libs(PKG_INIT,init=True)
    
    # build default tailwind.css
    echo("build generic tailwindcss file",blank=True)
    sp.shell(config.subproc['.tailwindcss'],
        cwd=f"{config.root_path}/webpages/resources")

    try:
        # provide sweetheart html documentation    
        os.symlink(f"{config.root_path}/documentation/sweetbook/book",
            f"{config.root_path}/webpages/sweetbook")

        # provide installed javascript libs within Ubuntu/Debian
        os.symlink("/usr/share/javascript",
            f"{config.root_path}/webpages/resources/javascript")
    except:
        verbose("INFO:\n an error occured creating symlinks during init process",
            "\n an expected cause could be that links are already existing")

    if "jupyter" in PKG_INIT['pylibs'] or "jupyterlab" in PKG_INIT['pylibs']:
        # set Jupyter service if needed
        from sweetheart.heart import JupyterLab
        echo("set the JupyerLab ipkernel and required password",blank=True)
        JupyterLab(config).set_ipykernel()
        if config.project == MASTER_MODULE: JupyterLab(config).set_password()
    else:
        # install at least ipython and ipykernel for convenience
        installer.poetry("ipython","ipykernel")
    
    echo("installation process completed",blank=True)

    
class BaseInstall:

    def __init__(self,config:BaseConfig):

        self.config = config
        self.packages_file = f"{config.root_path}/configuration/packages.json"

        if config.project != MASTER_MODULE:

            #FIXME: set a new python sub-project
            sp.poetry("new","my_python",cwd=f"{config.root_path}/programs")
            sp.poetry("add",MASTER_MODULE)#NOTE: this can be a fork of sweetheart
            sp.set_python_env(cwd=f"{config.root_path}/programs/my_python")

            with open(f"{config.root_path}/configuration/subproc.json","w") as fi:
                json.dump({'pyenv':config.python_env},fi)

    def apt(self,*libs:str,**kwargs):
        """ install distro packages using apt """

        echo("apt install:",*libs,blank=True)
        return sp.run("sudo","apt","install",*libs,**kwargs)

    def cargo(self,*libs:str,init=False,**kwargs):
        """ install rust crates using cargo """

        echo("cargo install:",*libs,blank=True)
        path = self.config.subproc['rustpath']
        if init: sp.run(f"{path}/rustup","update")
        return sp.run(f"{path}/cargo","install",*libs,**kwargs)
    
    def poetry(self,*libs:str,**kwargs):
        """ install python packages using poetry """

        echo("poetry add:",*libs,blank=True)
        return sp.poetry("add",*libs,**kwargs)

    def npm(self,*libs:str,init=False,**kwargs):
        """ install node modules using npm """

        # if init:
        #     # for installing a specific version of nodejs
        #     echo("set node.js:",node_source.split()[2])
        #     sp.shell(node_source)
        #     sp.shell("sudo apt install -y nodejs")

        echo("npm install:",*libs,blank=True)
        os.chdir(f"{self.config.root_path}/webpages/resources")
        if init: sp.run("npm","init","--yes")
        return sp.run("npm","install",*libs,**kwargs)

    def install_libs(self,libs:dict,init:bool=False):
        """ install given libs using apt,cargo,poetry,npm
            and download listed files from github if given
            no libs arg will set init process for new project """

        aptlibs = libs.get('aptlibs')
        if aptlibs: self.apt(*aptlibs)

        cargolibs = libs.get('cargolibs')
        if cargolibs: self.cargo(*cargolibs,init=init)

        npmlibs = libs.get('npmlibs')
        if npmlibs: self.npm(*npmlibs,init=init)

        pylibs = libs.get('pylibs')
        if pylibs: self.poetry(*pylibs)

        files = libs.get('files')
        if files: self.download(*files)

        # install package documentation if given
        documentation = libs.get('documentation')
        if documentation: self.unzip_doc(documentation)

    def download(self,*files_list:str):
        """ download given listed files from github """

        for relpath in files_list:
            echo("download file:",relpath)
            urlretrieve(urljoin(raw_github,relpath),
                os.path.join(self.config.root_path,relpath))
    
    def unzip_doc(self,zipfile:str,remove:bool=True):
        """ unzip and build documentation """

        os.chdir(f"{self.config.root_path}/documentation")
        name,ext = os.path.splitext(zipfile)
        assert ext == ".zip"

        with ZipFile(zipfile,"r") as zf: zf.extractall()
        sp.shell(f"{self.config.subproc['rustpath']}/mdbook build {name}")
        if remove: os.remove(zipfile)

    def install_packages(self,*packages:str):
        """ install selected sweetheart packages """

        with open(self.packages_file) as fi:
            json_pkg = json.load(fi)

        for pkg in packages:
            self.install_libs(json_pkg[pkg])
