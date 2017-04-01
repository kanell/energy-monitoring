// Helper Function in pure Javascript
var timers = [];
function clearTimers() {
    for (var i=0; i<timers.length; i++) {
        window.clearInterval(timers[i]);
    }
    timers = [];
}

// Request for Flask
function makeFlaskRequest (requestJSON, plotId) {
  let req = new XMLHttpRequest();
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

$(document).ready(function(){
  /* "Aktuelle Werte" */

  // Uebersicht wird geklickt
  $("#Uber_i").click(function(){
    // Verstecke nicht geklickte Seiten
    $("#Frequenz_i, #Spannung_i, #Strom_i, #Leistung_i, .Inhalt_hist, .Inhalt_analy").hide();
    // Zeige geklickte Seite
    $("#Ubersicht_i").show();
    changeColor(a="aktiv",b="oben", c="oben");
    // Beende alle Anfragen/Timer
    clearTimers()
    // Hole gesuchte Werte ab// Get data function
    function updateLiveDashboad() {
      $.ajax({
        cache: false,
        url: "temp/json/livedata.json",
        dataType: "json",
        success: function(data) {
          let input = data
          // Iterate over all needed ports
          for (i=1; i <= 3; i++) {
            var U = 806 + i*2;
            var I = 858 + i*2;
            var S = 882 + i*2;
            var P = 866 + i*2;
            var Q = 874 + i*2;
            var THD_U = 834 + i*2;
            var THD_I = 906 + i*2;
            var f = 800;
            // push data to table Id
            document.getElementById("U" + i + "t").innerHTML =  input["port_" + U] ;
            document.getElementById("I" + i + "t").innerHTML =  input["port_" + I] ;
            document.getElementById("S" + i + "t").innerHTML =  input["port_" + S] ;
            document.getElementById("P" + i + "t").innerHTML =  input["port_" + P] ;
            document.getElementById("Q" + i + "t").innerHTML =  input["port_" + Q] ;
            document.getElementById("THD_U" + i + "t").innerHTML =  input["port_" + THD_U];
            document.getElementById("THD_I" + i + "t").innerHTML =  input["port_" + THD_I];
            document.getElementById("ft").innerHTML =  input["port_" + f] ;
          };
        }
      });
    }
    function updateLiveDashboadRepeater() {
      updateLiveDashboad();
      timers.push(window.setInterval(function (){updateLiveDashboad();}, 1000));
    }
    updateLiveDashboadRepeater()
  });

  // Spannung wird geklickt
  $("#U_i").click(function(){
    $("#Frequenz_i, #Strom_i, #Ubersicht_i, #Leistung_i, .Inhalt_hist, .Inhalt_analy").hide();
    $("#Spannung_i").show();
    changeColor(a="aktiv",b="oben", c="oben");
    clearTimers()

    // set graph
    const currentVoltageOptions = {
      xValueParser : function(x) {return 1000 * parseFloat(x);},
      axes : {
        x : {
            valueFormatter : function(x) {return Dygraph.dateString_(x,0);},
            axisLabelFormatter : Dygraph.dateAxisLabelFormatter,
            ticker: Dygraph.dateTicker
        }
      }
    }
    let currentVoltageData = "timestamp,u1,u2,u3\n"
    let currentVoltageGraph = new Dygraph(document.getElementById("div_U"), currentVoltageData, currentVoltageOptions);
    function updateCurrentVoltageGraphRepeater () {
      function updateCurrentVoltageGraph () {
        $.ajax({
          type: "GET",
          cache: false,
          url: "temp/csv/voltage.csv",
          dataType: "text",
          success: function (data) {
            currentVoltageData = data;
            currentVoltageGraph.updateOptions({'file':currentVoltageData});
          }
        });
      }
      updateCurrentVoltageGraph()
      timers.push(window.setInterval(function (){updateCurrentVoltageGraph();}, 1000));
    }
    updateCurrentVoltageGraphRepeater()
  });

  // Frequenz wird geklickt
  $("#f_i").click(function(){
    $("#Spannung_i, #Strom_i, #Ubersicht_i, #Leistung_i, .Inhalt_hist, .Inhalt_analy").hide();
    $("#Frequenz_i").show();
    changeColor(a="aktiv",b="oben", c="oben");
    clearTimers()

    // set graph
    const currentFrequencyOptions = {
      xValueParser : function(x) {return 1000 * parseFloat(x);},
      axes : {
        x : {
            valueFormatter : function(x) {return Dygraph.dateString_(x,0);},
            axisLabelFormatter : Dygraph.dateAxisLabelFormatter,
            ticker: Dygraph.dateTicker
        }
      }
    }
    let currentFrequencyData = "timestamp,frequency\n"
    let currentFrequencyGraph = new Dygraph(document.getElementById("div_f"), currentFrequencyData, currentFrequencyOptions);
    function updateCurrentFrequencyGraphRepeater () {
      function updateCurrentFrequencyGraph () {
        $.ajax({
          type: "GET",
          cache: false,
          url: "temp/csv/frequency.csv",
          dataType: "text",
          success: function (data) {
            currentFrequencyData = data;
            currentFrequencyGraph.updateOptions({'file':currentFrequencyData});
          }
        });
      }
      updateCurrentFrequencyGraph()
      timers.push(window.setInterval(function (){updateCurrentFrequencyGraph();}, 1000));
    }
    updateCurrentFrequencyGraphRepeater()
  });


  // Strom wird geklickt
  $("#I_i").click(function(){
    $("#Frequenz_i, #Spannung_i, #Ubersicht_i, #Leistung_i, .Inhalt_hist, .Inhalt_analy").hide();
    $("#Strom_i").show();
    changeColor(a="aktiv",b="oben", c="oben");
    clearTimers()

    // set graph
    const currentCurrentOptions = {
      xValueParser : function(x) {return 1000 * parseFloat(x);},
      axes : {
        x : {
            valueFormatter : function(x) {return Dygraph.dateString_(x,0);},
            axisLabelFormatter : Dygraph.dateAxisLabelFormatter,
            ticker: Dygraph.dateTicker
        }
      }
    }
    let currentCurrentData = "timestamp,i1,i2,i3\n"
    let currentCurrentGraph = new Dygraph(document.getElementById("div_I"), currentCurrentData, currentCurrentOptions);
    function updateCurrentCurrentGraphRepeater () {
      function updateCurrentCurrentGraph () {
        $.ajax({
          type: "GET",
          cache: false,
          url: "temp/csv/current.csv",
          dataType: "text",
          success: function (data) {
            currentCurrentData = data;
            currentCurrentGraph.updateOptions({'file':currentCurrentData});
          }
        });
      }
      updateCurrentCurrentGraph()
      timers.push(window.setInterval(function (){updateCurrentCurrentGraph();}, 1000));
    }
    updateCurrentCurrentGraphRepeater()
  });


  // Leistung wird geklickt
  $("#L_i").click(function(){
    $("#Frequenz_i, #Spannung_i, #Ubersicht_i, #Strom_i, .Inhalt_hist, .Inhalt_analy").hide();
    $("#Leistung_i").show();
    changeColor(a="aktiv",b="oben", c="oben");
    clearTimers()

    // set graph
    const currentPowerOptions = {
      xValueParser : function(x) {return 1000 * parseFloat(x);},
      axes : {
        x : {
            valueFormatter : function(x) {return Dygraph.dateString_(x,0);},
            axisLabelFormatter : Dygraph.dateAxisLabelFormatter,
            ticker: Dygraph.dateTicker
        }
      }
    }
    let currentPowerData = "timestamp,p1,p2,p3\n"
    let currentPowerGraph = new Dygraph(document.getElementById("div_L"), currentPowerData, currentPowerOptions);
    function updateCurrentPowerGraphRepeater () {
      function updateCurrentPowerGraph () {
        $.ajax({
          type: "GET",
          cache: false,
          url: "temp/csv/power.csv",
          dataType: "text",
          success: function (data) {
            currentPowerData = data;
            currentPowerGraph.updateOptions({'file':currentPowerData});
          }
        });
      }
      updateCurrentPowerGraph()
      timers.push(window.setInterval(function (){updateCurrentPowerGraph();}, 1000));
    }
    updateCurrentPowerGraphRepeater()
  });

  /* Historische Werte */

  // Spannung wird geklickt
  $("#U_h").click(function(){
    $("#Frequenz_h, #Strom_h, #Leistung_h, #Harmonische_U_h, #Harmonische_I_h, .Inhalt_ist, .Inhalt_analy").hide();
    $("#Spannung_h").show();
    changeColor(a="oben",b="aktiv", c="oben");
    // Datepicker
    $("#datepicker_1").datepicker();
    // set graph
    const histoticVoltageOptions = {
      xValueParser : function(x) {return 1000 * parseFloat(x);},
      axes : {
        x : {
            valueFormatter : function(x) {return Dygraph.dateString_(x,0);},
            axisLabelFormatter : Dygraph.dateAxisLabelFormatter,
            ticker: Dygraph.dateTicker
        }
      }
    }
    let histoticVoltageData = "timestamp,u1,u2,u3\n"
    let histoticVoltageGraph = new Dygraph(document.getElementById("historic_chart_u"), histoticVoltageData, histoticVoltageOptions);
    function updateHistoricVoltageGraph(histoticVoltageGraph) {
      // create requestJSON
      var requestJSON = {
        date : document.getElementById("datepicker_1").value,
        dataName : "voltage"
      }
      // make request
      console.log(requestJSON);
      makeFlaskRequest(requestJSON, histoticVoltageGraph)
    }
    updateHistoricVoltageGraph(histoticVoltageGraph)
    $("#load_voltage").click(function(){
      updateHistoricVoltageGraph(histoticVoltageGraph)
    });
  });

  // Frequenz wird geklickt
  $("#f_h").click(function(){
    $("#Spannung_h, #Strom_h, #Leistung_h, #Harmonische_U_h, #Harmonische_I_h, .Inhalt_ist, .Inhalt_analy").hide();
    $("#Frequenz_h").show();
    changeColor(a="oben",b="aktiv", c="oben");
    clearIntervalFunction();
  });

  // Strom wird geklickt
  $("#I_h").click(function(){
    $("#Spannung_h, #Frequenz_h, #Leistung_h, #Harmonische_U_h, #Harmonische_I_h, .Inhalt_ist, .Inhalt_analy").hide();
    $("#Strom_h").show();
    changeColor(a="oben",b="aktiv", c="oben");
    clearIntervalFunction();
  });

  // Leistung wird geklickt
  $("#L_h").click(function(){
    $("#Spannung_h, #Frequenz_h, #Strom_h, #Harmonische_U_h, #Harmonische_I_h, .Inhalt_ist, .Inhalt_analy").hide();
    $("#Leistung_h").show();
    changeColor(a="oben",b="aktiv", c="oben");
    clearIntervalFunction();
  });

  // Harmonische Spannung werden geklickt
  $("#H_U_h").click(function(){
    $("#Spannung_h, #Frequenz_h, #Strom_h, #Leistung_h, #Harmonische_I_h, .Inhalt_ist, .Inhalt_analy").hide();
    $("#Harmonische_U_h").show();
    changeColor(a="oben",b="aktiv", c="oben");
    clearIntervalFunction();
  });

  // Harmonische Strom werden geklickt
  $("#H_I_h").click(function(){
    $("#Spannung_h, #Frequenz_h, #Strom_h, #Leistung_h, #Harmonische_U_h, .Inhalt_ist, .Inhalt_analy").hide();
    $("#Harmonische_I_h").show();
    changeColor(a="oben",b="aktiv", c="oben");
    clearIntervalFunction();
  });
  /* Analyse */

  // Spannung U1 wurde geklickt
  $("#U1_a").click(function(){
    $("#Spannung_2_a, #Spannung_3_a, #Frequenz_a, #Harmonische_U_a, #Harmonische_I_a, .Inhalt_ist, .Inhalt_hist").hide();
    $("#Spannung_1_a").show();
    changeColor(a="oben",b="oben", c="aktiv");
    clearIntervalFunction();
    Analyse();
  });

  // Spannung U2 wurde geklickt
  $("#U2_a").click(function(){
    $("#Spannung_1_a, #Spannung_3_a, #Frequenz_a, #Harmonische_U_a, #Harmonische_I_a, .Inhalt_ist, .Inhalt_hist").hide();
    $("#Spannung_2_a").show();
    changeColor(a="oben",b="oben", c="aktiv");
    clearIntervalFunction();
  });

  // Spannung U3 wurde geklickt
  $("#U3_a").click(function(){
    $("#Spannung_1_a, #Spannung_2_a, #Frequenz_a, #Harmonische_U_a, #Harmonische_I_a, .Inhalt_ist, .Inhalt_hist").hide();
    $("#Spannung_3_a").show();
    changeColor(a="oben",b="oben", c="aktiv");
    clearIntervalFunction();
  });

  // Frequenz wurde geklickt
  $("#f_a").click(function(){
    $("#Spannung_1_a, #Spannung_2_a, #Spannung_3_a, #Harmonische_U_a, #Harmonische_I_a, .Inhalt_ist, .Inhalt_hist").hide();
    $("#Frequenz_a").show();
    changeColor(a="oben",b="oben", c="aktiv");
    clearIntervalFunction();
  });

  // THD U wurde geklickt
  $("#THD_U_a").click(function(){
    $("#Spannung_1_a, #Spannung_2_a, #Spannung_3_a, #Frequenz_a, #Harmonische_I_a, .Inhalt_ist, .Inhalt_hist").hide();
    $("#Harmonische_U_a").show();
    changeColor(a="oben",b="oben", c="aktiv");
    clearIntervalFunction();
  });

  // THD I wurde geklickt
  $("#THD_I_a").click(function(){
    $("#Spannung_1_a, #Spannung_2_a, #Spannung_3_a, #Frequenz_a, #Harmonische_U_a, .Inhalt_ist, .Inhalt_hist").hide();
    $("#Harmonische_I_a").show();
    changeColor(a="oben",b="oben", c="aktiv");
    clearIntervalFunction();
  });
  // click to show dashboard at start
  document.getElementById("Uber_i").click();
});

/* Changes the Color of the selected Tab */
function changeColor() {
  document.getElementById("aktuell").className = a;
  document.getElementById("historisch").className = b;
  document.getElementById("analysiert").className = c;
}

// clear all Intervals
function clearIntervalFunction() {
  if (Interval_U_t == 1) {window.clearInterval(Interval_U); Interval_U_t = 0;}
  if (Interval_I_t == 1) {window.clearInterval(Interval_I); Interval_I_t = 0;}
  if (Interval_f_t == 1) {window.clearInterval(Interval_f); Interval_f_t = 0;}
  if (Interval_Table_t == 1) {window.clearInterval(Interval_Table); Interval_Table_t = 0;}
  if (Interval_L_t == 1) {window.clearInterval(Interval_L); Interval_L_t = 0;}
}
