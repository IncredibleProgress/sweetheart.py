# sweetheart.py

## Introduction

Since Ubuntu 20.04 can be installed as usual softwares within windows 10, it provides an incredible way for any organization to develop, administrate, deploy powerfull webapps on its own local network and giving high capabilities of integration with already existing tools. Sweetheart will propose a simple and efficient approach to do it leading you to the best coding practices.

### sweetheart provides highest quality components and aims to be adopted by newbies:

- easy to learn, easy to use
- full documentation provided
- quick and clean prototyping
- quick and clean deployement
- ready for maintenable great code quality
- ready for datacenters, big-data and ai
- ready for inovation and creativity

sweetheart is python/html/css centric meaning that you can do a lot by yourself and you will find support and skilled people everywhere for lowest costs (e.g. projects with studients)

### sweetheart provides supercharged basis available for your non-expert hands :

- provided database server: MongoDB
- provided webservers: Uvicorn, CherryPy
- responsive user interfaces: Html
- backend language: Python3
- frontend language: Typescript
- provided libs for going fast: Knacss, W3css
- provided libs for high-level featuring: Bootstrap4, Vue.js
- all others nice things you wish using apt, pip and npm

start now using same raw materials of gafam and go farer ahead !

## Write your first webapp

### your first standalone webpage conroller

``` python
import sweet

def welcome():
    """render a welcome message"""
    return sweet.html()

sweet.quickstart(welcome)
```

open a terminal and launch ```sweet my-first-webapp```

### your first pythonic html webpage

``` html
% rebase("sweet.HTML")

<div class="txtcenter">
    <br>
    <h1>Welcome!</h1>
    <br>
    <p>get now coding full power at the speedlight</p>
    <p><button id="btn" class="btn" onclick="click()">click here</button></p>
</div>

<script type="text/python">
from browser import document

def click(event):
    # change text within the button when clicked
    event.target.text = "fired!"

document["btn"].bind("click", click)
</script>
```
