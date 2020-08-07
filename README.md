# sweetheart.py

allow building of full-stacked webapps including AI at the speedlight

## Introduction

Since Ubuntu20.04 can be installed as a usual softwares within Windows10, it provides an incredible way for any organization to develop, administrate and deploy **powerfull responsive webapps** on its own local network **including AI** and high capabilities of integration with the already existing tools like databases, ms-excel, sap...

The sweetheart framework propose a simple and efficient approach to do it in a python/html/css centric way leading you to the best components and coding practices. Due to the current place of the python language regarding to data handling, calculations and AI, this makes sweetheart a fast and ideal toolkit for evoluting towards the **Industry4.0** precepts .

## The highest quality components that can be adopted by newbies

- easy to learn, easy to use
- full documentation provided
- built-in reponsive user interfaces
- quick and clean prototyping
- quick and clean deployement
- ready for maintenable great code quality
- **ready for datacenters, big-data and AI**
- **ready for inovation and creativity**

## A supercharged heart for the non-expert hands

- backend language: [Python3](https://www.python.org/)
- provided database server: [**MongoDB**](https://www.mongodb.com/)
- provided asynchronous webserver: [Uvicorn](https://www.uvicorn.org/)
- optionnal webserver for static contents: [CherryPy](https://cherrypy.org/)
- provided asgi frameworks that shines: [Starlette](https://www.starlette.io/)
- optionnal asgi framework for big projects: [FastApi](https://fastapi.tiangolo.com/)
- responsive user interfaces: [Html](https://www.w3schools.com/)
- provided web libs for going fast: [**Knacss**](https://www.knacss.com/), [W3css](https://www.w3schools.com/w3css/)
- provided web libs for high-level featuring: [Bootstrap4](https://getbootstrap.com/), [Vue.js](https://vuejs.org/)
- optionnal frontend language: [Typescript](https://www.typescriptlang.org/)

**And all other nice things you wish using apt, pip and npm:** sweetheart comes with the above mentionned package to support you saving a lot of time. Your are not force to use these components, but these are what you should highly consider at first for starting new projects.

## Code examples

### your first standalone webpage conroller

```python
import sweet

def welcome():
    """render a welcome message"""
    return sweet.html()

sweet.quickstart(welcome)
```

### your first *sweet* html webpage

``` html
% rebase("sweet.HTML")

<div class="txtcenter">
    <h1>Welcome!</h1>
    <p>get coding full power at the speedlight</p>
</div>
```
