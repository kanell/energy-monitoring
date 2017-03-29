$(document).ready(function(){
  // Datepicker
  $(function() {
    $("#datepicker").datepicker();
  });

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
  var voltagePlot = new Dygraph(document.getElementById("historic_chart_u"), [[0],[0],[0],[0]],plotOptions);

  // Request for Flask
  function makeFlaskRequest(requestJSON){
    var req = new XMLHttpRequest();
    function transferComplete() {
      console.log(req.responseText);
      //voltagePlot.updateOptions( { 'file': req.responseText } );
      }
    req.addEventListener('load',transferComplete);
    req.open('POST', '/get_data');
    req.setRequestHeader('Content-Type', 'application/json;charset=UTF-8');
    req.responseType = 'text';
    req.send(JSON.stringify(requestJSON));
  }

  // Init Plot
  function loadHistoricVoltageData() {
    // create requestJSON
    var requestJSON = {
      startTime : 1,
      endTime : 2,
      dataName : 'Voltage'
    }
    // make request
    makeFlaskRequest(requestJSON)
  }
}
