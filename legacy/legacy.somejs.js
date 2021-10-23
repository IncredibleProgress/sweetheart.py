
    // // set table facilities
    // rowMark = 'm'; colMark = 'd';
    // function getRowFromId(id=null) {
    //   if (id == null) { var id = event.target.id };
    //   var ir = id.indexOf(rowMark); 
    //   var ic = id.indexOf(colMark);
    //   if (ir < ic) { var ir2 = ic } else { var ir2 = id.length };
    //   return parseInt(id.slice(ir+1,ir2))
    // }
    // function getColFromId(id=null) {
    //   if (id == null) { var id = event.target.id };
    //   var ir = id.indexOf(rowMark);
    //   var ic = id.indexOf(colMark);
    //   if (ir < ic) { var ic2 = id.length } else { var ic2 = ir };
    //   return parseInt(id.slice(ic+1,ic2))
    // }
    // function getIdFromRowCol(row,col) {
    //   return rowMark+toString(row)+colMark+toString(col)
    // }

    // vuedata = {v:{}};
    // document.addEventListener("DOMContentLoaded",function(){
    //   vueapp = Vue.createApp ({
    //     data() { return vuedata },
    //   }).mount('#vue');
    //   try { v = vueapp.v } catch(err) {};
    //   % if "py" in load:
    //   brython({% get('__debug__',0) %});
    //   % end
    // })