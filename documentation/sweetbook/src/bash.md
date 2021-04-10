# Bash
*the linux shell power in your hands*

## SWeet Shell commands

    sws sweet --init        #install default sweetheart components 
    sws install <package>   #install additionnal resources
    sws start -j            #start and discover sweeheart and jupyter
    sws python              #get ipython shell in dedicated virtual env
    sws poetry add <module> #install new python module in dedicated virtual env

## File system commands

### working directory

    cd <path>   #change current directory to the <path> directory
    cd ~        #change current directory to your default user directory
    cd ~/<path> #change to an existing <path> into your default user directory
    cd ..       #change current directory to the parent directory
    cd ../..    #change current directory to the parent of the parent directory
    cd <match>* #change current directory to first directory starting with <match>

### list files within a directory

    ls          #list your files in the current directory
    ls <dir>    #list your files in the given directory <dir>
    ls -l       #list your files in the current dir with details
    ls -l <dir> #list your files in the given directory <dir> 
