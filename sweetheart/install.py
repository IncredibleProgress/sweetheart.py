
from sweetheart.globals import *

from zipfile import ZipFile
from urllib.parse import urljoin
from urllib.request import urlretrieve


wsl_rustup = "curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh"
raw_github = "https://raw.githubusercontent.com/IncredibleProgress/sweetheart.py/master/"# / is needed
get_poetry = "curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python3 -"
get_prereq = "curl -sSL https://raw.githubusercontent.com/IncredibleProgress/sweetheart.py/master/get-sweetheart.py | python3 -"


# ensure prerequisites
if os.path.isfile(
    f"{os.environ['HOME']}/.sweet/{SWEETHEART}/programs/my_python/pyproject.toml"):
        verbose("install: existing prerequisites found")
else:
    sp.shell(get_prereq)


def init(config:BaseConfig):
    """ set require configuration before sweetheart installation
        and intends to provide minimalistic sweetheart features """

    PKG_INIT = { 
        'npmlibs': ["brython"],
        'documentation': "sweetbook.zip",
        'cargolibs': ["mdbook","mdbook-toc"],
        'aptlibs': ["xterm","rustc","mongodb","npm"],
        'pylibs': ["bottle","pymongo","uvicorn","aiofiles","starlette","jupyter"],
        'files': ["configuration/packages.json","webpages/HTML","documentation/sweetbook.zip"] }

    # require directories
    for basedir in [
        f"{config.root_path}/configuration",
        f"{config.root_path}/database",
        f"{config.root_path}/documentation/notebooks",
        #f"{config.root_path}/documentation/sweetbook",
        f"{config.root_path}/programs/scripts",
        f"{config.root_path}/webpages/templates",
        f"{config.root_path}/webpages/resources",
        #f"{config.root_path}/webpages/markdown",
    ]: os.makedirs(basedir,exist_ok=True)

    # install default libs
    installer = BaseInstall(config)
    installer.install_libs(PKG_INIT,init=True)

    try:
        # provide installed javascript libs (Ubuntu)
        os.symlink("/usr/share/javascript",
            f"{config.root_path}/webpages/resources/javascript")

        # provide sweetheart html documentation    
        os.symlink(f"{config.root_path}/documentation/sweetbook/book",
            f"{config.root_path}/webpages/sweetbook")
    except:
        verbose("INFO:\n an error occured creating symlinks during init process",
            "\n an expected cause could be that links are already existing")

    # set JupyterLab service
    from sweetheart.heart import Notebook
    echo("set the JupyerLab ipkernel and required password",blank=True)
    jupyter = Notebook(config)
    jupyter.set_ipykernel()

    if config.project == SWEETHEART:
        jupyter.set_password()

    
class BaseInstall:

    def __init__(self,config:BaseConfig):

        self.config = config
        self.packages_file = f"{config.root_path}/configuration/packages.json"

        if config.project != SWEETHEART:

            sp.poetry("new","my_python",cwd=f"{config.root_path}/programs")
            sp.poetry("add",SWEETHEART)
            sp.set_python_env(cwd=f"{config.root_path}/programs/my_python")

            with open(f"{config.root_path}/configuration/subproc.json","w") as fi:
                json.dump({'pyenv':config.python_env},fi)

    def apt(self,*libs:str,**kwargs):
        """ install distro packages using apt """

        echo("apt install:",*libs)
        return sp.run("sudo","apt","install",*libs,**kwargs)

    def cargo(self,*libs:str,**kwargs):
        """ install rust crates using cargo """

        echo("cargo install:",*libs)
        path = self.config.subproc['rustpath']
        return sp.run(f"{path}/cargo","install",*libs,**kwargs)
    
    def poetry(self,*libs:str,**kwargs):
        """ install python packages using poetry """

        echo("poetry add:",*libs)
        return sp.poetry("add",*libs,**kwargs)

    def npm(self,*libs:str,init=False,**kwargs):
        """ install node modules using npm """

        echo("npm install:",*libs)
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
        if cargolibs: self.cargo(*cargolibs)

        pylibs = libs.get('pylibs')
        if pylibs: self.poetry(*pylibs)

        npmlibs = libs.get('npmlibs')
        if npmlibs: self.npm(*npmlibs,init=init)

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
