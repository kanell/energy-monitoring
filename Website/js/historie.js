
var date_1 = "";
var date_2 = "";

$(document).ready(function(){
  // Datepicker

  $("#datepicker_1").datepicker( {
  onSelect: function(date) {
      date_1 = date;
  },});
 
  $("#datepicker_2").datepicker( {
  onSelect: function(date) {
      date_2 = date;
  },});
 
  /* Load plots */
  // Voltage plot
  var voltagePlotOptions = {xValueParser : function(x) {return 1000 * parseFloat(x);},
    axes : {
    x : {
        valueFormatter : function(x) {return Dygraph.dateString_(x,0);},
        axisLabelFormatter : Dygraph.dateAxisLabelFormatter,
        ticker: Dygraph.dateTicker
      }
    }
  }
  var voltagePlot = new Dygraph(document.getElementById("historic_chart_u"), [[0],[0],[0],[0]],voltagePlotOptions);
});

// Request for Flask
function makeFlaskRequest(requestJSON){
  var req = new XMLHttpRequest();
  function transferComplete() {
    console.log(req.responseText);
    //voltagePlot.updateOptions( { 'file': req.responseText } );
    }
  req.addEventListener('load',transferComplete);
  req.open('POST', '/get_data/');
  req.setRequestHeader('Content-Type', 'application/json;charset=UTF-8');
  req.responseType = 'text';
  req.send(JSON.stringify(requestJSON));
}

// Init Plot
function loadHistoricVoltageData() {
  // create requestJ,SON
  var requestJSON = {
    startTime : date_1,
    endTime : date_2,
    dataName : "Voltage"
  }
  // make request
  console.log(requestJSON);
  makeFlaskRequest(requestJSON)
}
