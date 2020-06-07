# sweetheart.py

## Introduction

Since Ubuntu 20.04 can be installed as usual softwares within windows 10, it provides an incredible way for any organization to develop, administrate, deploy webapps on its own local network and giving high capabilities of integration with the already existing tools.

### sweetheart provides highest quality components and aims to be adopted by newbies:

- easy to learn, easy to use
- quick and clean prototyping
- quick and clean deployement
- ready for maintenable great code quality
- ready for datacenters, big-data and ai
- ready for inovation and creativity

sweetheart is python/html/css centric meaning that you can do a lot by yourself
and that you will find support and skilled people everywhere for lowest costs
(e.g. projects with studients)

### sweetheart provides supercharged basis available for your non-expert hands :

- provided database server: MongoDB
- provided webserver: CherryPy
- responsive user interfaces: Html
- backend language: Python3
- frontend language: Typescript
- provided libs for going fast: Knacss W3css
- provided libs for high-level featuring: Bootstrap4 Vue.js
- all others nice things you wish using apt, pip and npm

start now using raw materials of gafam and go farer ahead !

## Write your first webapp

``` python
import sweetheart

class myFirstApp():
    """ a webpages controller """

    @sweetheart.expose()
    def default(self):
        """ render a welcome message """
        return sweetheart.html()

sweetheart.start( myFirstApp() )
```