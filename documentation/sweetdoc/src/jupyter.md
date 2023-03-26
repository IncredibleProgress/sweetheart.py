# Jupyter Lab

``` bash
jupyter notebook --no-browser --notebook-dir=/path/to/notebooks/dir
jupyterlab --no-browser --notebook-dir=/path/to/notebooks/dir
jupyter notebook password -y

ipykernel install --user --name myenv 
ipykernel install --user --name myenv  --display-name "myenv"

jupyter kernelspec list
jupyter kernelspec remove mykernel
```