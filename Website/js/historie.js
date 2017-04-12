$(document).ready(function(){
  // Datepicker
  $("#datepicker_1").datepicker();
});

function VoltageChart_h() {
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
    return voltagePlot;
};


// Request for Flask
function makeFlaskRequest(requestJSON, plotId){
  var req = new XMLHttpRequest();
  function transferComplete() {
    console.log(req.responseText);
    plotId.updateOptions( { 'file': req.responseText } );
    }
  req.addEventListener('load',transferComplete);
  req.open('POST', '/get_data/');
  req.setRequestHeader('Content-Type', 'application/json;charset=UTF-8');
  req.responseType = 'text';
  req.send(JSON.stringify(requestJSON));
}

// Init Plot
function loadHistoricVoltageData(plotId) {
  // create requestJSON
  var requestJSON = {
    date : document.getElementById("datepicker_1").value,
    dataName : "voltage"
  }
  // make request
  console.log(requestJSON);
  makeFlaskRequest(requestJSON, plotId)
}
