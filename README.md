# Sweetheart

allow building full-stacked webapps including AI at the speedlight

## Introduction

Since *Ubuntu 20.04* can be installed as a usual softwares within *Windows 10*, it provides an incredible way for any organization to develop, administrate and deploy **powerfull responsive webapps** on its own local network **including AI** keeping high capabilities of integration with the already existing tools like databases, ms-excel, sap...

The sweet(heart) script provides a simple and efficient approach to do it in a python/html/css centric way leading you to the best components and **best coding practices**. Due to the current place of the python language regarding to data handling, calculations and AI, this makes sweetheart a fast and ideal toolkit for evoluting towards the **Industry4.0** precepts .

Sweetheart is shared under the [CeCILL-C FREE SOFTWARE LICENSE AGREEMENT](https://github.com/IncredibleProgress/sweetheart.py/blob/master/LICENSE).

## A supercharged heart for the non-expert hands

Sweetheart help you to get coding full power from scratch:

- easy to learn, easy to use
- full documentation provided
- built-in reponsive user interfaces
- quick and clean prototyping
- quick and clean deployement
- ready for maintenable great code quality
- **ready for datacenters, big-data and AI**
- **ready for inovation and creativity**

## The highest quality components that can be adopted by newbies

Ready to use features for starting your projects:

- backend language: [**Python3**](https://www.python.org/)
- provided database server: [**MongoDB**](https://www.mongodb.com/)
- provided asynchronous webserver: [Uvicorn](https://www.uvicorn.org/)
- optionnal webserver for static contents: [CherryPy](https://cherrypy.org/)
- provided asgi framework that shines: [**Starlette**](https://www.starlette.io/)
- optionnal asgi framework built on Starlette: [FastApi](https://fastapi.tiangolo.com/)
- responsive user interfaces: [Html](https://www.w3schools.com/)
- provided web libs for going fast: [**Knacss**](https://www.knacss.com/), [W3css](https://www.w3schools.com/w3css/)
- provided web libs for high-level featuring: [Bootstrap4](https://getbootstrap.com/), [Vue.js](https://vuejs.org/)
- optionnal frontend language: [Typescript](https://www.typescriptlang.org/)

**And all other nice things you wish using apt, pip and npm:** sweetheart comes with the above mentionned package to support you saving time. Your are not forced to use these components, but these are what you should highly consider at first for starting new projects.

## The sweetheart developpement chart

Next table allow to evaluate coding and costs efforts at the statement of sweetheart today.

| Matters                                      | Coding effort | Costs effort |
| :------------------------------------------- | :-----------: | :----------: |
| Build responsive webapp with default libs    | FAST          | FREE         |
| Build responsive webapp with bootstrap4      | MIDDLE        | FREE         |
| Run MongoDB/webserver on local network       | FAST          | FREE         |
| Run MongoDB/webserver as internet services   | MIDDLE        | MODERATE     |
| Improve code quality and reinforce security  | EXPERT        | CHEAP        |
| Implement AI capabilities                    | MIDDLE        | MODERATE     |
| Implement SAP gateway                        | MIDDLE        | MODERATE     |
| Erect and run a dedicated datacenter         | EXPERT        | HIGH         |

## Code examples

### your first standalone webpage controller written in Python

``` python
import sweet

def welcome():
    """render a welcome message"""
    return sweet.html()

sweet.quickstart(welcome)
```

### your first *sweet* Html webpage including a bit of KNACss

``` html
% rebase("sweet.HTML")

<div class="txtcenter">
    <h1>Welcome!</h1>
    <p>get coding full power at the speedlight</p>
</div>
```

## Install sweetheart

On *Windows 10* you have first to open the *Windows Store* for installing **Ubuntu 20.04 LTS** and the **Windows Terminal**.

Generally speaking sweetheart runs on *Ubuntu 20.04 LTS*. It will works on other *Linux OS* but it requires in this case some manual tasks for installing usefull dependencies.

Opening an Ubuntu terminal, the 3 following lines will do all what is needed:

``` sh
sudo apt install python3-pip
pip3 install sweetheart
python3 -m sweet --init
```

Note that all resources are now located within the `/opt/sweetheart` directory. Have a look on it now could help you in the next steps for quicker understanding of what is doing sweetheart under the hood.

Now start a standalone welcome webapp to ensure that everything is working well. With the provided initial config the following command will work only on *Windows 10* with *Windows Terminal* and *Edge* installed.

``` sh
sweet start --webapp
```

In other cases omit the `--webapp` option and open manually the indicated url in a webbrowser.
