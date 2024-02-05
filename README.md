!! Sweetheart 0.1.3 coming soon with new enhancements:
   - *basement re-written with Rust, great ideas made with Python remains*
   - *new way for building powerfull app using React and Typescript*
    
# Sweetheart **0.1.2** (deprecated)
*innovative foundations for rugged and enterprise-grade solutions*

## A supercharged heart for the non-expert hands

What about security, big-data, real-time databases, responsive interfaces and AI? Sweetheart comes with the highest quality components widely used by GAFAM and others, also the best coding practices, and makes the hard stuff for you. Start from scratch, and create with ease and efficiency the apps you really need embedding reliable open-source code for processing at full power data which remains yours!

Since Ubuntu and RHEL based operating systems can be installed as usual software within Windows 10/11, it provides an incredible way for any organization to develop, deploy, and administrate powerful responsive apps including AI on its own local network keeping high capabilities of integration with the already existing tools like databases, MS-Excel, and SAP.

Sweetheart provides a simple Python/Html centric approach leading you implementing best components and best practices. Due to the top-rated place of the Python language regarding to data processing, calculations and AI, this makes sweetheart a fast and ideal toolkit for innovative ideas.

Sweetheart is shared under the [CeCILL-C FREE SOFTWARE LICENSE AGREEMENT](https://github.com/IncredibleProgress/sweetheart.py/blob/master/LICENSE).

## Get coding full power including AI at the light speed

Sweetheart supports you getting coding full power from scratch:

  - easy to learn, easy to use
  - full documentation provided
  - built-in responsive user interfaces
  - quick and clean prototyping
  - quick and clean deployment
  - made for maintainable great code quality
  - made for calculations, big-data and AI
  - made for high performances and innovation

## Stick to good standards without thinking about it

Sweetheart is a thin-layer for going efficient and doesn't reinvent the wheel. It intends to transform you stepwise in a good driver and maybe in a pilot! Due to provided high quality components, a hardened configuration and the included documentation you will **learn quickly to make great python/html code** including up-to-date best practices and patterns. You won't learn Sweetheart itself, you will learn Python/Html real coding-life like any other developer, but skipping some tedious considerations. That means especially you don't need any kind of expertise to use good things in the right way. Be quite, Sweetheart is made for low resources consumption, high security level, and best performances:

  - it ensures code reliability and maintainability
  - it ensures an enterprise-grade security level
  - it ensures ruggedness of the committed libraries
  - it ensures the efficiency of your coding effort
  - it allows you to operate without cloud services

## Rock-solid components for supporting innovative capabilities

Sweetheart allows you to do all what you need with only 1 Python file and 1 Html file, that's it! Even more, it leads you writing in a natural low-code and minimalistic way. Behind the proposed Python/Html centric approach a stock of ready-to-use features are delivered. Under the hood it integrates the most powerful and innovative features at the time being: **Nginx Unit - RethinkDB - Jupyter - TailwindCss - Vue - WebSocket - Rust Crates**

Nevertheless it remains feasible to add any other nice things you wish using dedicated tools like [poetry](https://python-poetry.org/), [npm](https://docs.npmjs.com/about-npm/), [apt](https://en.wikipedia.org/wiki/APT_(software)) and [cargo](https://doc.rust-lang.org/cargo/). Sweetheart comes with the above mentioned package to support you saving huge amount of time and strengthen the foundations of your project. Your are not forced to use these components, but these are what you should highly consider before starting new developments.

### why RethinkDB ?

Maybe some of you can be surprised with regards to RethinkDB, because this not currently the best known database server. Believe it will become one of these within next years. Sweetheart intends to provide a NoSQL and JSON-based database for performances and versatility purposes as MongoDB can be today. In comparison RethinkDB won't support big binaries like MongoDB can do, but this is not a concern for considered enterprise solutions here. On the other hand collaborative work between people must be considered at the highest level in any enterprise and organization. Meaning that working together on same data using several devices has to be the normal way, not a big challenge. Usually implementing real-time capabilities on database systems is technically sophisticated. Because originally the involved technologies were not made for such expectations. RethinkDB is designed for it. Furthermore admin interface is great, queries made with ReQL are great, no need of any ORM, and no SQL injection attacks risk.

## Realistic code examples

### typical webpage controller written in Python

``` python
from sweetheart.sandbox import *

config = set_config({
    "db_name": "test" })

webapp = HttpServer(config, set_database=True).app(
    Route("/", TemplateResponse("table_example.htm")) )
```

### typical Html webpage template

``` html
<!SWEETHEART html>

<python>
# this is brython here, waiting stable releases of py-script
# sweetheart preset RethinkDB/WebSocket/Vue3 capabilities for you

def on_update(event):

    """ this updates in realtime RethinkDB using WebSocket 
        it should be called only from html event attributes
        e.g. <input type="text" id="row:col" v-on:keyup="update">
        you see, we handle directly the JavaScript event object """

    elt = event.target
    
    r.table("grid")
    r.filter({"id": elt.tableId})
    r.update({elt.tableCol: elt.value})

def on_message(event):

    """ catch here WebSocket messages from the server side """

    console.log(event.data)

def vue_created(data):

    """ this will be called as soon as the Vue3 instance is created
        it allows you fetching data using ReQL before html rendering
        the data argument provides the $data object of the Vue model """

    r.table("grid").setVueAttr("table")

createVueApp({
    "table": [],# content comes within vue_created()
    "headers": ["col1","col2","col3"]
})
</python>

<vue>
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
          <input type="text" v-bind:id="tableId(n,h)" v-model="table[n][h]" v-on:keyup="update">
        </td>
      </tr>
    </tbody>
  </table>
</vue>
```

## Install and run Sweetheart

### set WSL on Windows 10/11

Discovering what is the WSL, have a look at the [Microsoft documentation](https://docs.microsoft.com/en-us/windows/wsl/about). Then install *Ubuntu 22.04* via the Microsoft Store. At this step installing *VS Code* and *Windows Terminal* can be recommended to you too. When done click on Ubuntu within start menu, and now *Bash* is running!

### first steps with Bash

1. start setting the prerequisites
``` bash
curl -sSL https://raw.githubusercontent.com/IncredibleProgress/sweetheart.py/master/sweetheart/install.py | python3 -
```

2. then (re)start bash and get initial components
``` bash
bash
sws init
```

3. at last run sweetheart for tests
``` bash
sws start
```

<!-- ### get power with many additional resources

``` bash
# interested for calculation, machine-learning, ms-excel
sws install science

# interested for processing or scraping the web
sws install web
``` -->

## Epilogue: a new life starts now

Even at this beta stage, Sweetheart allows you to make a lot by yourself. Enjoy discovering and learning how coding can help and support you, using amazing raw materials widely used by GAFAM and others!
