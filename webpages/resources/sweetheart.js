// TODO: script not yet implemented
// provide data exchange capabilities
class DataHub {
  constructor(dbname) {
    this.apiversion = "0.1.0";
    this.route = `/data/${dbname}`;
    const host = "{%__host__%}".replace("https","ws").replace("http","ws");
    this.websocket = new WebSocket(`${host}${this.route}`);
    document.addEventListener("unload",()=>this.websocket.close());
    this.websocket.onmessage = (event) => this.onmessage(event);
  }
  fetchJSON(scope) {
    return fetch("/data", {
      method: "POST",
      headers: {
        "Content-Type": "application/json" },
      body: JSON.stringify({
        info: {
          "title": "sweetAPI",
          "version": this.apiversion },
        header: {
          "service": "fetch|JSON|<ELEMENT>",
          "database": this.dbname,
          "expected": "JSON" },
        data: {
          //sql: scope.sql,
          //find: scope.find,
          "reql": this.reql,
          "target": scope.target },
      })
    }).then(response => response.json())
  }
  setVueAttr(attr) {
    this.fetchJSON({ "target": `vmodel.$data.${attr}` })
      .then(json => eval(`${json.data.target} = json.data.value`))
  }
  sendJSON(service,data) {
    this.websocket.send(JSON.stringify({
      info: {
          "title": "sweetAPI",
          "version": this.apiversion },
      header: {
          "service": service,
          "database": this.dbname,
          "expected": "JSON" },
      data: data,
    }))
  }
}
// provide ReQL capabilities
class RethinkDB extends DataHub {
  constructor(dbname) {
    super(dbname);
    this.dbname = dbname;
    this.updateAndSend = true;
  }
  table(tablename) {
    // init a new RethinkDB query 
    this.tablename = tablename;
    this.filterJSON = undefined;
    this.updateJSON = undefined;
    this.reql = `table("${this.tablename}")`;
    return this
  }
  count(arg="") {
    this.reql += `.count(${arg.toString()})`;
    return this
  }
  filter(json) {
    this.filterarg = json;
    this.filterJSON = JSON.stringify(json);
    this.reql += `.filter(${this.filterJSON})`;
    return this
  }
  update(json) {
    this.updateJSON = JSON.stringify(json);
    this.reql += `.update(${this.updateJSON})`;
    if ( this.updateAndSend == true ) { this.sendJSON(
      "ws|ReQL.UPDATE|<LOG>",{
        "table": this.tablename,
        "filter": this.filterJSON,
        "update": this.updateJSON })
    };
  }
}
r = new RethinkDB("{%__dbnm__%}");

// set default Vue3 utilities
function setVueData(vuedata, options={vm:"vdata", id:"VueApp"}) {
      // set data only within the vue model
      document.addEventListener("DOMContentLoaded",function(){
      let vm = Vue.createApp({ data() {return vuedata} }).mount(`#${options.id}`);
      eval(`${options.vm} = vm`);
    })
  }
function createVueApp(vuedata, options={
      vm: "vmodel", id: "VueApp", hub: r
    }) {
  if ( typeof(vuedata) == "object" ) {
    // should be a JavaScript function call case
    // here vuedata allows setting the entire vue model
    document.addEventListener("DOMContentLoaded",function(){
      let vm = Vue.createApp(vuedata).mount(`#${options.id}`);
      eval(`${options.vm} = vm`);
    })
  } else if ( typeof(vuedata) == "string" ) {
    // should be a Brython function call case
    let vm = Vue.createApp({
      data() { return JSON.parse(vuedata) },
      created() { try {vuecreated(this.$data)} catch(err){} },
      methods: { 
        update(event) { 
          const sep = event.target.id.indexOf(":");
          event.target.tableRowId = event.target.id.slice(0,sep);
          event.target.tableColHeader = event.target.id.slice(sep+1);
          options.hub.onupdate(event);
        },
        tableId(row,header) {
          const vm = eval(`${options.vm}`);
          return `${vm.table[row]['id']}:${header}`
        }
      }
    }).mount(`#${options.id}`);
    eval(`${options.vm} = vm`);
  }
}