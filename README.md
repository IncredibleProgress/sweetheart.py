# Sweetheart **0.1.1**
*get power with low-code and low-costs python programs*

## A supercharged heart for the non-expert hands

What about safety, big-data, realtime databases, responsive interfaces and AI? Sweetheart comes with the highest quality components widely used by GAFAM and others, also the best coding practices, and makes the hard stuff for you. Start from scratch, and create with ease and efficiency the apps you really need embedding reliable open-source code for processing at full power data which remains yours!

Since Ubuntu 20.04 can be installed as usual softwares within Windows 10, it provides an incredible way for any organization to develop, deploy, and administrate **powerful responsive webapps including AI** on its own local network keeping high capabilities of integration with the already existing tools like databases, MS-Excel, and SAP.

Sweetheart provides a simple Python/Html centric approach leading you implementing best components and best coding practices. Due to the top-rated place of the Python language regarding to data processing, calculations and AI, this makes sweetheart a fast and ideal toolkit to e-volute towards **Industry4.0** precepts and innovative ideas.

Sweetheart is shared under the [CeCILL-C FREE SOFTWARE LICENSE AGREEMENT](https://github.com/IncredibleProgress/sweetheart.py/blob/master/LICENSE).

## Get coding full power including AI at the light speed

Sweetheart supports you getting coding full power from scratch:

- easy to learn, easy to use
- full documentation provided
- built-in responsive user interfaces
- quick and clean prototyping
- quick and clean deployment
- ready for maintenable great code quality
- ready for datacenters, big-data and AI
- ready for high performances, innovation and creativity

## Stick to good standards without thinking about it

Sweetheart is a thin-layer for going efficient and doesn't reinvent the wheel. It just intends to transform you stepwise in a good driver and maybe in a pilot! Due to provided components, configuration and documentation **you will learn quickly to make great python/html code** including up-to-date best practices and patterns. You won't learn Sweetheart itself, you will learn Python/Html real programming life like any other developer, but gradually and under control. Meaning that you don't need any kind of expertise to use the good things in the right way.

## The highest quality components which can be adopted by newbies

Sweetheart delivers a stock of ready-to-use features:

- backend language: [Python](https://www.python.org/)
- database server: [RethinkDB](https://rethinkdb.com)
- asgi framework: [Starlette](https://www.starlette.io/)
- asynchronous webserver: [Uvicorn](https://www.uvicorn.org/)
- fast documentation builder: [mdBook](https://rust-lang.github.io/mdBook/index.html)
- responsive user interfaces: [Html](https://www.w3schools.com/), [JupyterLab](https://jupyter.org/)
- web libs for going fast: [TailwindCss](https://tailwindcss.com/), [Vue](https://v3.vuejs.org/)

**And all other nice things you wish** using [poetry](https://python-poetry.org/), [npm](https://docs.npmjs.com/about-npm/), [apt](https://en.wikipedia.org/wiki/APT_(software)) and [cargo](https://doc.rust-lang.org/cargo/): Sweetheart comes with the above mentioned package to support you saving time. Your are not forced to use these components, but these are what you should highly consider for starting new projects.

In a first approach consider it provides to you **an incredible full-stacked sandbox**. In a second time you will take benefits of Sweetheart as a convenient super-orchestrator for low-costs.

## Keep permanently innovative capabilities

The following *sweetheart development chart* allows to evaluate coding and costs efforts for implementation of most important and innovative features at the date of today.

|                                              | Coding effort | Costs effort |
| :------------------------------------------- | :-----------: | :----------: |
| Build responsive webapp with default libs    | FAST          | FREE         |
| Build responsive datavisualizations          | MIDDLE        | FREE         |
| Run MongoDB/webserver on local network       | FAST          | FREE         |
| Improve code quality and reinforce security  | EXPERT        | CHEAP        |
| Run MongoDB/webserver as internet services   | MIDDLE        | MODERATE     |
| Implement AI capabilities                    | MIDDLE        | MODERATE     |
| Implement SAP gateway                        | MIDDLE        | MODERATE     |
| Erect and run a dedicated datacenter         | EXPERT        | HIGH         |

## Realistic code examples

Sweetheart allows you to do all what you need with only 1 Python file and 1 Html file, that's it! Even more, it leads you writting in a natural low-code and minimalistic way. Neithertheless under the hood it integrates the most powerfull and innovative features at the time being like Ubuntu, Rust, RethinkDB, Jupyter, TailwindCss and Vue.

### typical webpage controller written in Python

``` python
from sweetheart.sandbox import *

config = set_config({
    "webbrowser": "brave.exe",
    "selected_DB": "test" })

webapp = HttpServer(config, set_database=True).mount(
    Route("/", HTMLTemplate("grid.htm")) )

quickstart(webapp)
```

### typical Html webpage template

``` html
<!SWEETHEART html>

<python>
# some nice python code can be given here (many thanks to Brython!)
# SweetHeart preset also RethinkDB/WebSocket/Vue3 capabilities for you

def on_update(event):

    """ this updates in realtime RethinkDB using WebSocket 
        it should be called only from html event attributes
        e.g. <input type="text" id="row:col" v-on:keyup="update"> """

    elt = event.target
    
    r.table("grid")
    r.filter({"id": elt.tableId})
    r.update({elt.tableCol: elt.value})

def on_message(event):

    """ catch here WebSocket messages from the server side 
        you see, we handle directly the JavaScript event object """

    console.log(event.data)

def vue_created(data):

    """ this will be called as soon as the Vue3 instance is created
        it allows you fecthing data using ReQL before html rendering
        the data argument provides the $data object of the Vue model """

    r.table("grid").setVueAttr("table")

createVueApp({
    "table": [],
    "headers": ["col1","col2","col3"]
})
</python>

<div v-cloak id="VueApp" class="m-2">
  <h1 class="text-xl">Realtime Table</h1>

  <table>
    <thead>
      <tr>
        <th v-for="h in headers" class="border">{{ h }}</th>
      </tr>
    </thead>
    <tbody>
      <tr v-for="n in table.length">
        <td v-for="h in headers" class="border">
          <input type="text" v-bind:id="tableId(n-1,h)" v-model="table[n-1][h]" v-on:keyup="update">
        </td>
      </tr>
    </tbody>
  </table>
</div>
```

## Install and run Sweetheart

### set WSL on Windows 10

Discovering what is the WSL, have a look at the [Microsoft documentation](https://docs.microsoft.com/en-us/windows/wsl/about). Then install *Ubuntu 20.04* via the Microsoft Store. At this step installing *VS Code* and *Windows Terminal* can be recommended to you too. When done click on Ubuntu within start menu, and now *Bash* is running!

### first steps with Bash

1. start setting the prerequisites
``` bash
curl -sSL https://raw.githubusercontent.com/IncredibleProgress/sweetheart.py/master/get-sweetheart.py | python3 - --rethinkdb
```
You can suppress the `--rethinkdb` option if you don't need to setup the RethinkDB repository for Ubuntu/Debian.

2. then restart bash and get initial components
``` bash
bash
sws --init
```
Being experienced you can add extra python libs you want with `--init`. Typically you could prefer `fastapi` instead of simply `starlette`. Note too that Jupyter is not set in by default. This is because you could already use it by another way (e.g. within VS Code). If not you should also consider to install it with sweetheart as showed hereafter.

``` bash
# alternative examples for initial setting of sweetheart
sws --init jupyter
sws --init fastapi
sws --init fastapi jupyter
```

3. at last run sweetheart for tests
``` bash
sws start
```

There is here no heavy installation process which could badly interact with the operating system. Everything goes and runs safely within dedicated */home* directories. [Click-here]() for detailed informations.

### get power with many additionnal resources

``` bash
# interested for calculation, machine-learning, ms-excel
sws install science

# interested for processing or scraping the web
sws install web
```

## Epilogue: a new life starts now

Even at this BETA stage, Sweetheart allows you to make a lot by yourself. Enjoy discovering and learning how coding can help and support you, using amazing raw materials widely used by GAFAM and others!
