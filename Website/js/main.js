// Helper Function in pure Javascript
var timers = [];
function clearTimers() {
  for (var i=0; i<timers.length; i++) {
    window.clearTimeout(timers[i]);
  }
  timers = [];
}

function legendFormatter(data) {
  if (data.x == null) {
    if (data.dygraph.rawData_.length == 0) {return}
    let t;
    // Abfrage ob Harmonische oder nicht
    if (data.dygraph.rawData_.length != 39) {
      t = data.dygraph.rawData_.length - 1;
    }
    else {
      t = 1
      var x_Value_label = data.dygraph.rawData_;
    }
    let firstDataPoint = data.dygraph.rawData_[t];
    maxData = firstDataPoint.length;
    for (var i=1; i < maxData; i++) {
      data.series[i-1]['firstDataPoint']= firstDataPoint[i];
    }
    x=firstDataPoint[0]
    // Abfrage ob Harmonische oder nicht
    if (data.dygraph.rawData_.length != 39) {
      var x_Value_Label = Dygraph.dateString_(x,0);
    }
    else {
      var x_Value_Label = '2. Harmonische'
    }
    // This happens when there's no selection and {legend: 'always'} is set.
  	return  x_Value_Label + '<br>' + data.series.map(function(series) { return series.dashHTML + ' ' + '<b style="color: ' + series.color + '">' + series.labelHTML + '</b>: ' + series.firstDataPoint }).join('<br>') + '<br>' + '<br>';
  }
  if (data.dygraph.rawData_.length != 39) {
    var html = data.xHTML
  }
  else {
    var html =  data.xHTML + '. Harmonische';
  }
  data.series.forEach(function(series) {
    if (!series.isVisible) {return};
    var labeledData = '<b style="color: ' + series.color + '">' + series.labelHTML + '</b>: ' + series.yHTML;
    if (series.isHighlighted) {
      labeledData = '<b>' + labeledData + '</b>';
    }
    html += '<br>' + series.dashHTML + ' ' + labeledData ;
  });
  html += '<br>' + '<br>';
  return html;
}

function barChartPlotter(e) {
  if (e.seriesIndex !== 0) return;
  var g = e.dygraph;
  var ctx = e.drawingContext;
  var sets = e.allSeriesPoints;
  var y_bottom = e.dygraph.toDomYCoord(0);
  // Find the minimum separation between x-values.
  // This determines the bar width.
  var min_sep = Infinity;
  for (var j = 0; j < sets.length; j++) {
    var points = sets[j];
    for (var i = 1; i < points.length; i++) {
      var sep = points[i].canvasx - points[i - 1].canvasx;
      if (sep < min_sep) min_sep = sep;
    }
  }
  var bar_width = Math.floor(2.0 / 3 * min_sep);
  var fillColors = g.getColors();
  var strokeColors = g.getColors();
  for (var j = 0; j < sets.length; j++) {
    ctx.fillStyle = fillColors[j];
    ctx.strokeStyle = strokeColors[j];
    for (var i = 0; i < sets[j].length; i++) {
      var p = sets[j][i];
      var center_x = p.canvasx;
      var x_left = center_x - (bar_width / 2) * (1 - j/(sets.length-1));
      ctx.fillRect(x_left, p.canvasy,
          bar_width/sets.length, y_bottom - p.canvasy);
      ctx.strokeRect(x_left, p.canvasy,
          bar_width/sets.length, y_bottom - p.canvasy);
    }
  }
}

// Request for Flask
function makeFlaskRequest (requestJSON, plotId, plotData) {
  let req = new XMLHttpRequest();
  function transferComplete() {
    //console.log(req.responseText);
    plotData = req.responseText;
    plotId.updateOptions({
      'file': plotData,
      dateWindow: null,
      valueRange: null
    });
  }
  req.addEventListener('load',transferComplete);
  req.open('POST', '/get_data/');
  req.setRequestHeader('Content-Type', 'application/json;charset=UTF-8');
  req.responseType = 'text';
  req.send(JSON.stringify(requestJSON));
}

// Download All function
function downloadAll(requestJSON){
  let req = new XMLHttpRequest();
  function transferComplete() {
    console.log(req.response);
    let blob = new Blob([this.response], {type: 'octet-stream'});
    let a = document.createElement('a');
    a.href = window.URL.createObjectURL(blob)
    a.download = 'data.csv';
    a.style.display = 'none';
    document.body.appendChild(a)
    a.click()
  }
  req.addEventListener('load',transferComplete);
  req.open('POST', '/get_data/');
  req.setRequestHeader('Content-Type', 'application/json;charset=UTF-8');
  req.responseType = 'blob';
  req.send(JSON.stringify(requestJSON));
}

// download selected data
function downloadSelected(plotData) {
  let blob = new Blob([plotData], {type: 'octet-stream'});
  let a = document.createElement('a');
  a.href = window.URL.createObjectURL(blob)
  a.download = 'data.csv';
  a.style.display = 'none';
  document.body.appendChild(a)
  a.click()
}

// get deviation table data from flask
function makeFlaskRequestDeviationTable(tableId, requestJSON){
  let req = new XMLHttpRequest();
  // insert data to deviation table
  function appendToTable(){
    console.log(req.response);
    let trHTML = '<tr class="UberschreitungsTabelle"><th class="UberschreitungsTabelle">Zeitstempel</th><th>Wert</th><th>Abweichung in %</th></tr>';
    $.each(req.response, function (i, item) {
      trHTML += '<tr><td>' + item.timestamp + '</td><td>' + item.value + '</td><td>' + item.deviation + '</td></tr>';
    });
    tableId.innerHTML = trHTML;
  }
  req.addEventListener('load',appendToTable);
  req.open('POST', '/get_data/analyse');
  req.setRequestHeader('Content-Type', 'application/json;charset=UTF-8');
  req.responseType = 'json';
  req.send(JSON.stringify(requestJSON));
}
function updateFlaskRequestDeviationTable(tableId, dataPhase, dataName){
  let requestJSON = {
    dataName : dataName,
    dataPhase : dataPhase
  };
  makeFlaskRequestDeviationTable(tableId, requestJSON);
}

$(document).ready(function(){
  /* "Aktuelle Werte" */

  // Uebersicht wird geklickt
  $("#Uber_i").click(function(){
    // Verstecke nicht geklickte Seiten
    $("#Frequenz_i, #Spannung_i, #Strom_i, #Leistung_i, #Harmonische_I_i, #Harmonische_U_i, .Inhalt_hist, .Inhalt_analy").hide();
    // Zeige geklickte Seite
    $("#Ubersicht_i").show();
    changeColor(a="aktiv",b="oben", c="oben");
    // Beende alle Anfragen/Timer
    clearTimers();
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
            document.getElementById("U" + i + "t").innerHTML =  input["port_" + U];
            document.getElementById("I" + i + "t").innerHTML =  input["port_" + I];
            document.getElementById("S" + i + "t").innerHTML =  input["port_" + S];
            document.getElementById("P" + i + "t").innerHTML =  input["port_" + P];
            document.getElementById("Q" + i + "t").innerHTML =  input["port_" + Q];
            document.getElementById("THD_U" + i + "t").innerHTML =  input["port_" + THD_U];
            document.getElementById("THD_I" + i + "t").innerHTML =  input["port_" + THD_I];
            document.getElementById("ft").innerHTML =  input["port_" + f];
          };
          timers.push(window.setTimeout(function (){updateLiveDashboad();}, 1000));
        }
      });
      $.ajax({
        cache: false,
        url: "temp/json/liveanalyse.json",
        dataType: "json",
        success: function(data) {
          let input = data
          // Iterate over all needed ports
          for (i=1; i <= 3; i++) {
            // push data to table Id
            document.getElementById("Norm_U" + i + "t").innerHTML =  input["voltage_L" + i];
            document.getElementById("Norm_I" + i + "t").innerHTML =  1;
            document.getElementById("Norm_S" + i + "t").innerHTML =  1;
            document.getElementById("Norm_P" + i + "t").innerHTML =  1;
            document.getElementById("Norm_Q" + i + "t").innerHTML =  1;
            document.getElementById("Norm_THD_U" + i + "t").innerHTML =  1;
            document.getElementById("Norm_THD_I" + i + "t").innerHTML =  1;
            document.getElementById("Norm_ft").innerHTML =  1;
          };
          timers.push(window.setTimeout(function (){updateLiveDashboad();}, 1000));
        }
      });
    }
    updateLiveDashboad()
  });

  // Spannung wird geklickt
  $("#U_i").click(function(){
    $("#Frequenz_i, #Strom_i, #Ubersicht_i, #Leistung_i, #Harmonische_I_i, #Harmonische_U_i, .Inhalt_hist, .Inhalt_analy").hide();
    $("#Spannung_i").show();
    changeColor(a="aktiv",b="oben", c="oben");
    clearTimers();

    // set graph
    const currentVoltageOptions = {
      xValueParser : function(x) {return 1000 * parseFloat(x);},
      xlabel : 'Uhrzeit',
      ylabel : 'Spannung [V]',
      digitsAfterDecimal : 4,
      axes : {
        x : {
            valueFormatter : function(x) {return Dygraph.dateString_(x,0);},
            axisLabelFormatter : Dygraph.dateAxisLabelFormatter,
            ticker: Dygraph.dateTicker
        }
      },
      labelsDiv: document.getElementById('legend_U_i'),
      legend: 'always',
      legendFormatter: legendFormatter
    }

    let currentVoltageData = "timestamp,u1,u2,u3\n"
    let currentVoltageGraph = new Dygraph(document.getElementById("div_U"), currentVoltageData, currentVoltageOptions);
    function updateCurrentVoltageGraph () {
      $.ajax({
        type: "GET",
        cache: false,
        url: "temp/csv/voltage.csv",
        dataType: "text",
        success: function (data) {
          // if-Abfrage zur Überprüfung der Vollständigkeit des Datensatzes
          if (currentVoltageData.length <= data.length) {
            currentVoltageData = data;
            currentVoltageGraph.updateOptions({'file':currentVoltageData});
          }
          timers.push(window.setTimeout(function (){updateCurrentVoltageGraph();}, 1000));
        }
      });
    }
    updateCurrentVoltageGraph()
  });

  // Frequenz wird geklickt
  $("#f_i").click(function(){
    $("#Spannung_i, #Strom_i, #Ubersicht_i, #Leistung_i, #Harmonische_I_i, #Harmonische_U_i, .Inhalt_hist, .Inhalt_analy").hide();
    $("#Frequenz_i").show();
    changeColor(a="aktiv",b="oben", c="oben");
    clearTimers();

    // set graph
    const currentFrequencyOptions = {
      xValueParser : function(x) {return 1000 * parseFloat(x);},
      xlabel : 'Uhrzeit',
      ylabel : 'Frequenz [Hz]',
      digitsAfterDecimal : 4,
      axes : {
        x : {
            valueFormatter : function(x) {return Dygraph.dateString_(x,0);},
            axisLabelFormatter : Dygraph.dateAxisLabelFormatter,
            ticker: Dygraph.dateTicker
        }
      },
      labelsDiv: document.getElementById('legend_f_i'),
      legend: 'always',
      legendFormatter: legendFormatter
    }
    let currentFrequencyData = "timestamp,frequency\n"
    let currentFrequencyGraph = new Dygraph(document.getElementById("div_f"), currentFrequencyData, currentFrequencyOptions);
    function updateCurrentFrequencyGraph () {
      $.ajax({
        type: "GET",
        cache: false,
        url: "temp/csv/frequency.csv",
        dataType: "text",
        success: function (data) {
          // if-Abfrage zur Überprüfung der Vollständigkeit des Datensatzes
          if (currentFrequencyData.length <= data.length) {
            currentFrequencyData = data;
            currentFrequencyGraph.updateOptions({'file':currentFrequencyData});
          }
          timers.push(window.setTimeout(function (){updateCurrentFrequencyGraph();}, 1000));
        }
      });
    }
    updateCurrentFrequencyGraph()
  });


  // Strom wird geklickt
  $("#I_i").click(function(){
    $("#Frequenz_i, #Spannung_i, #Ubersicht_i, #Leistung_i, #Harmonische_I_i, #Harmonische_U_i, .Inhalt_hist, .Inhalt_analy").hide();
    $("#Strom_i").show();
    changeColor(a="aktiv",b="oben", c="oben");
    clearTimers();

    // set graph
    const currentCurrentOptions = {
      xValueParser : function(x) {return 1000 * parseFloat(x);},
      xlabel : 'Uhrzeit',
      ylabel : 'Strom [A]',
      digitsAfterDecimal : 4,
      axes : {
        x : {
            valueFormatter : function(x) {return Dygraph.dateString_(x,0);},
            axisLabelFormatter : Dygraph.dateAxisLabelFormatter,
            ticker: Dygraph.dateTicker
        }
      },
      labelsDiv: document.getElementById('legend_I_i'),
      legend: 'always',
      legendFormatter: legendFormatter
    }
    let currentCurrentData = "timestamp,i1,i2,i3\n"
    let currentCurrentGraph = new Dygraph(document.getElementById("div_I"), currentCurrentData, currentCurrentOptions);
    function updateCurrentCurrentGraph () {
      $.ajax({
        type: "GET",
        cache: false,
        url: "temp/csv/current.csv",
        dataType: "text",
        success: function (data) {
          // if-Abfrage zur Überprüfung der Vollständigkeit des Datensatzes
          if (currentCurrentData.length <= data.length) {
            currentCurrentData = data;
            currentCurrentGraph.updateOptions({'file':currentCurrentData});
          }
          timers.push(window.setTimeout(function (){updateCurrentCurrentGraph();}, 1000));
        }
      });
    }
    updateCurrentCurrentGraph()
  });


  // Leistung wird geklickt
  $("#L_i").click(function(){
    $("#Frequenz_i, #Spannung_i, #Ubersicht_i, #Strom_i, #Harmonische_I_i, #Harmonische_U_i, .Inhalt_hist, .Inhalt_analy").hide();
    $("#Leistung_i").show();
    changeColor(a="aktiv",b="oben", c="oben");
    clearTimers();

    // set graph
    const currentPowerOptions = {
      xValueParser : function(x) {return 1000 * parseFloat(x);},
      xlabel : 'Uhrzeit',
      ylabel : 'Leistung [W]',
      digitsAfterDecimal : 4,
      axes : {
        x : {
            valueFormatter : function(x) {return Dygraph.dateString_(x,0);},
            axisLabelFormatter : Dygraph.dateAxisLabelFormatter,
            ticker: Dygraph.dateTicker
        }
      },
      labelsDiv: document.getElementById('legend_L_i'),
      legend: 'always',
      legendFormatter: legendFormatter
    }
    let currentPowerData = "timestamp,p1,p2,p3\n"
    let currentPowerGraph = new Dygraph(document.getElementById("div_L"), currentPowerData, currentPowerOptions);
    function updateCurrentPowerGraph () {
      $.ajax({
        type: "GET",
        cache: false,
        url: "temp/csv/power.csv",
        dataType: "text",
        success: function (data) {
          // if-Abfrage zur Überprüfung der Vollständigkeit des Datensatzes
          if (currentPowerData.length <= data.length) {
            currentPowerData = data;
            currentPowerGraph.updateOptions({'file':currentPowerData});
          }
          timers.push(window.setTimeout(function (){updateCurrentPowerGraph();}, 1000));
        }
      });
    }
    updateCurrentPowerGraph()
  });

  // Harmonische U wird geklickt
  $("#H_U_i").click(function(){
    $("#Frequenz_i, #Strom_i, #Ubersicht_i, #Leistung_i, #Harmonische_I_i, #Spannung_i, .Inhalt_hist, .Inhalt_analy").hide();
    $("#Harmonische_U_i").show();
    changeColor(a="aktiv",b="oben", c="oben");
    clearTimers();

    // set graph
    const currentHarmonicVoltageOptions = {
      digitsAfterDecimal : 4,
      plotter: barChartPlotter,
      dateWindow: [1,40],
      labelsDiv: document.getElementById('legend_H_U_i'),
      legend: 'always',
      legendFormatter: legendFormatter
    }

    let currentHarmonicVoltageData = 'number,u1,u2,u3\n'
    let currentHarmonicVoltageGraph = new Dygraph(document.getElementById("div_H_U"), currentHarmonicVoltageData, currentHarmonicVoltageOptions);
    function updateCurrentHarmonicVoltageGraph () {
      $.ajax({
        type: "GET",
        cache: false,
        url: "temp/csv/harmonics_u.csv",
        dataType: "text",
        success: function (data) {
          currentHarmonicVoltageData = data;
          currentHarmonicVoltageGraph.updateOptions({'file':currentHarmonicVoltageData});
          timers.push(window.setTimeout(function (){updateCurrentHarmonicVoltageGraph();}, 1000));
        }
      });
    }
    updateCurrentHarmonicVoltageGraph()
  });

 // Harmonische I wird geklickt
  $("#H_I_i").click(function(){
    $("#Frequenz_i, #Strom_i, #Ubersicht_i, #Leistung_i, #Harmonische_U_i, #Spannung_i, .Inhalt_hist, .Inhalt_analy").hide();
    $("#Harmonische_I_i").show();
    changeColor(a="aktiv",b="oben", c="oben");
    clearTimers();

    // set graph
    const currentVoltageOptions = {
      xValueParser : function(x) {return 1000 * parseFloat(x);},
      xlabel : 'Uhrzeit',
      ylabel : 'Spannung [V]',
      digitsAfterDecimal : 4,
      axes : {
        x : {
            valueFormatter : function(x) {return Dygraph.dateString_(x,0);},
            axisLabelFormatter : Dygraph.dateAxisLabelFormatter,
            ticker: Dygraph.dateTicker
        }
      },
      labelsDiv: document.getElementById('legend_H_I_i'),
      legend: 'always',
      legendFormatter: legendFormatter
    }

    let currentVoltageData = "timestamp,u1,u2,u3\n"
    let currentVoltageGraph = new Dygraph(document.getElementById("div_H_I"), currentVoltageData, currentVoltageOptions);
    function updateCurrentVoltageGraph () {
      $.ajax({
        type: "GET",
        cache: false,
        url: "temp/csv/voltage.csv",
        dataType: "text",
        success: function (data) {
          currentVoltageData = data;
          // if-Abfrage zur Überprüfung der Vollständigkeit des Datensatzes
          if (currentVoltageData.length > 60000) {
            currentVoltageGraph.updateOptions({'file':currentVoltageData});
          }
          timers.push(window.setTimeout(function (){updateCurrentVoltageGraph();}, 1000));
        }
      });
    }
    updateCurrentVoltageGraph()
  });

  /* Historische Werte */

  // Spannung wird geklickt
  $("#U_h").click(function(){
    $("#Frequenz_h, #Strom_h, #Leistung_h, #Harmonische_U_h, #Harmonische_I_h, .Inhalt_ist, .Inhalt_analy").hide();
    $("#Spannung_h").show();
    changeColor(a="oben",b="aktiv", c="oben");
    clearTimers();
    // Datepicker
    $("#datepicker_1").datepicker();
    // set default startTime and endTime
    let startTime = Date.parse(new Date().toLocaleDateString('en-US')) / 1000
    let endTime = Date.parse(new Date()) / 1000
    let dataSize = 1000;
    // set graph
    const historicVoltageOptions = {
      xValueParser : function(x) {return 1000 * parseFloat(x);},
      zoomCallback : function() {
        startTime = historicVoltageGraph.xAxisRange()[0] / 1000;
        endTime = historicVoltageGraph.xAxisRange()[1] / 1000;
        updateHistoricVoltageGraph(historicVoltageGraph);
      },
      xlabel : 'Uhrzeit',
      ylabel : 'Spannung [V]',
      digitsAfterDecimal : 4,
      axes : {
        x : {
            valueFormatter : function(x) {return Dygraph.dateString_(x,0);},
            axisLabelFormatter : Dygraph.dateAxisLabelFormatter,
            ticker: Dygraph.dateTicker
        }
      },
      labelsDiv: document.getElementById('legend_U_h'),
      legend: 'always',
      legendFormatter: legendFormatter
    }
    let historicVoltageData = "timestamp,u1,u2,u3\n"
    let historicVoltageGraph = new Dygraph(document.getElementById("historic_chart_u"), historicVoltageData, historicVoltageOptions);
    function updateHistoricVoltageGraph(historicVoltageGraph, historicVoltageData) {
      dataSize = 1000;
      // create requestJSON
      let requestJSON = {
        startTime : startTime,
        endTime : endTime,
        dataName : "voltage",
        dataSize : dataSize,
        dataType : 'text'
      }
      // make request
      console.log(requestJSON);
      makeFlaskRequest(requestJSON, historicVoltageGraph, historicVoltageData)
    }
    updateHistoricVoltageGraph(historicVoltageGraph, historicVoltageData)
    function resetHistoricVoltageGraph(historicVoltageGraph, historicVoltageData) {
      if (document.getElementById("datepicker_1").value == ''){
        startTime = Date.parse(new Date().toLocaleDateString('en-US')) / 1000;
      } else {
        startTime = Date.parse(document.getElementById("datepicker_1").value) / 1000;
      }
      endTime = startTime + 24 * 60 * 60
      updateHistoricVoltageGraph(historicVoltageGraph, historicVoltageData);
    }
    $("#load_voltage").click(function(){
      resetHistoricVoltageGraph(historicVoltageGraph, historicVoltageData);
    });
    $("#historic_chart_u").dblclick(function(){
      resetHistoricVoltageGraph(historicVoltageGraph, historicVoltageData);
    });
    $("#download_all_voltage").click(function(){
      dataSize = 0;
      // create requestJSON
      let requestJSON = {
        startTime : startTime,
        endTime : endTime,
        dataName : "voltage",
        dataSize : dataSize,
        dataType : 'blob'
      }
      downloadAll(requestJSON);
    });
    $("#download_selected_voltage").click(function(){
      downloadSelected(historicVoltageData);
    });
  });

  // Frequenz wird geklickt
  $("#f_h").click(function(){
    $("#Spannung_h, #Strom_h, #Leistung_h, #Harmonische_U_h, #Harmonische_I_h, .Inhalt_ist, .Inhalt_analy").hide();
    $("#Frequenz_h").show();
    changeColor(a="oben",b="aktiv", c="oben");
    clearTimers();
    // Datepicker
    $("#datepicker_2").datepicker();
    // set default startTime and endTime
    let startTime = Date.parse(new Date().toLocaleDateString('en-US')) / 1000;
    let endTime = Date.parse(new Date()) / 1000;
    let dataSize = 1000;
    // set graph
    const historicFrequencyOptions = {
      xValueParser : function(x) {return 1000 * parseFloat(x);},
      zoomCallback : function() {
        startTime = historicFrequencyGraph.xAxisRange()[0] / 1000;
        endTime = historicFrequencyGraph.xAxisRange()[1] / 1000;
        updateHistoricFrequencyGraph(historicFrequencyGraph);
      },
      xlabel : 'Uhrzeit',
      ylabel : 'Frequenz [Hz]',
      digitsAfterDecimal : 4,
      axes : {
        x : {
            valueFormatter : function(x) {return Dygraph.dateString_(x,0);},
            axisLabelFormatter : Dygraph.dateAxisLabelFormatter,
            ticker: Dygraph.dateTicker
        }
      },
      labelsDiv: document.getElementById('legend_f_h'),
      legend: 'always',
      legendFormatter: legendFormatter
    }
    let historicFrequencyData = "timestamp,frequency\n"
    let historicFrequencyGraph = new Dygraph(document.getElementById("historic_chart_f"), historicFrequencyData, historicFrequencyOptions);
    function updateHistoricFrequencyGraph(historicFrequencyGraph, historicFrequencyData) {
      dataSize = 1000;
      // create requestJSON
      let requestJSON = {
        startTime : startTime,
        endTime : endTime,
        dataName : "frequency",
        dataSize : dataSize,
        dataType : 'text'
      }
      // make request
      console.log(requestJSON);
      makeFlaskRequest(requestJSON, historicFrequencyGraph, historicFrequencyData)
    }
    updateHistoricFrequencyGraph(historicFrequencyGraph, historicFrequencyData)
    function resetHistoricFrequencyGraph(historicFrequencyGraph, historicFrequencyData) {
      if (document.getElementById("datepicker_2").value == ''){
        startTime = Date.parse(new Date().toLocaleDateString('en-US')) / 1000
      } else {
        startTime = Date.parse(document.getElementById("datepicker_2").value) / 1000
      }
      endTime = startTime + 24 * 60 * 60
      updateHistoricFrequencyGraph(historicFrequencyGraph, historicFrequencyData)
    }
    $("#load_frequency").click(function(){
      resetHistoricFrequencyGraph(historicFrequencyGraph, historicFrequencyData)
    });
    $("#historic_chart_f").dblclick(function(){
      resetHistoricFrequencyGraph(historicFrequencyGraph, historicFrequencyData)
    });
    $("#download_all_frequency").click(function(){
      dataSize = 0;
      // create requestJSON
      let requestJSON = {
        startTime : startTime,
        endTime : endTime,
        dataName : "frequency",
        dataSize : dataSize,
        dataType : 'blob'
      }
      downloadAll(requestJSON);
    });
    $("#download_selected_frequency").click(function(){
      downloadSelected(historicFrequencyData);
    });
  });

  // Strom wird geklickt
  $("#I_h").click(function(){
    $("#Spannung_h, #Frequenz_h, #Leistung_h, #Harmonische_U_h, #Harmonische_I_h, .Inhalt_ist, .Inhalt_analy").hide();
    $("#Strom_h").show();
    changeColor(a="oben",b="aktiv", c="oben");
    clearTimers();
    // Datepicker
    $("#datepicker_3").datepicker();
    // set default startTime and endTime
    let startTime = Date.parse(new Date().toLocaleDateString('en-US')) / 1000;
    let endTime = Date.parse(new Date()) / 1000;
    let dataSize = 1000;
    // set graph
    const historicCurrentOptions = {
      xValueParser : function(x) {return 1000 * parseFloat(x);},
      zoomCallback : function() {
        startTime = historicCurrentGraph.xAxisRange()[0] / 1000;
        endTime = historicCurrentGraph.xAxisRange()[1] / 1000;
        updateHistoricCurrentGraph(historicCurrentGraph);
      },
      xlabel : 'Uhrzeit',
      ylabel : 'Strom [A]',
      digitsAfterDecimal : 4,
      axes : {
        x : {
            valueFormatter : function(x) {return Dygraph.dateString_(x,0);},
            axisLabelFormatter : Dygraph.dateAxisLabelFormatter,
            ticker: Dygraph.dateTicker
        }
      },
      labelsDiv: document.getElementById('legend_I_h'),
      legend: 'always',
      legendFormatter: legendFormatter
    }
    let historicCurrentData = "timestamp,i1,i2,i3\n"
    let historicCurrentGraph = new Dygraph(document.getElementById("historic_chart_i"), historicCurrentData, historicCurrentOptions);
    function updateHistoricCurrentGraph(historicCurrentGraph, historicCurrentData) {
      dataSize = 1000;
      // create requestJSON
      let requestJSON = {
        startTime : startTime,
        endTime : endTime,
        dataName : "current",
        dataSize : dataSize,
        dataType : 'text'
      }
      // make request
      console.log(requestJSON);
      makeFlaskRequest(requestJSON, historicCurrentGraph, historicCurrentData)
    }
    updateHistoricCurrentGraph(historicCurrentGraph, historicCurrentData)
    function resetHistoricCurrentGraph(historicCurrentGraph, historicCurrentData){
      if (document.getElementById("datepicker_3").value == ''){
        startTime = Date.parse(new Date().toLocaleDateString('en-US')) / 1000
      } else {
        startTime = Date.parse(document.getElementById("datepicker_3").value) / 1000
      }
      endTime = startTime + 24 * 60 * 60
      updateHistoricCurrentGraph(historicCurrentGraph, historicCurrentData)
    }
    $("#load_current").click(function(){
      resetHistoricCurrentGraph(historicCurrentGraph, historicCurrentData)
    });
    $("#historic_chart_i").dblclick(function(){
      resetHistoricCurrentGraph(historicCurrentGraph, historicCurrentData)
    });
    $("#download_all_current").click(function(){
      dataSize = 0;
      // create requestJSON
      let requestJSON = {
        startTime : startTime,
        endTime : endTime,
        dataName : "current",
        dataSize : dataSize,
        dataType : 'blob'
      }
      downloadAll(requestJSON);
    });
    $("#download_selected_current").click(function(){
      downloadSelected(historicCurrentData);
    });
  });

  // Leistung wird geklickt
  $("#L_h").click(function(){
    $("#Spannung_h, #Frequenz_h, #Strom_h, #Harmonische_U_h, #Harmonische_I_h, .Inhalt_ist, .Inhalt_analy").hide();
    $("#Leistung_h").show();
    changeColor(a="oben",b="aktiv", c="oben");
    clearTimers();
    // Datepicker
    $("#datepicker_4").datepicker();
    // set default startTime and endTime
    let startTime = Date.parse(new Date().toLocaleDateString('en-US')) / 1000;
    let endTime = Date.parse(new Date()) / 1000;
    let dataSize = 1000;
    // set graph
    const historicPowerOptions = {
      xValueParser : function(x) {return 1000 * parseFloat(x);},
      zoomCallback : function() {
        startTime = historicPowerGraph.xAxisRange()[0] / 1000;
        endTime = historicPowerGraph.xAxisRange()[1] / 1000;
        updateHistoricPowerGraph(historicPowerGraph);
      },
      xlabel : 'Uhrzeit',
      ylabel : 'Leistung [W]',
      digitsAfterDecimal : 4,
      axes : {
        x : {
            valueFormatter : function(x) {return Dygraph.dateString_(x,0);},
            axisLabelFormatter : Dygraph.dateAxisLabelFormatter,
            ticker: Dygraph.dateTicker
        }
      },
      labelsDiv: document.getElementById('legend_L_h'),
      legend: 'always',
      legendFormatter: legendFormatter
    }
    let historicPowerData = "timestamp,p1,p2,p3\n"
    let historicPowerGraph = new Dygraph(document.getElementById("historic_chart_p"), historicPowerData, historicPowerOptions);
    function updateHistoricPowerGraph(historicPowerGraph, historicPowerData) {
      dataSize = 1000;
      // create requestJSON
      let requestJSON = {
        startTime : startTime,
        endTime : endTime,
        dataName : "power",
        dataSize : dataSize,
        dataType : 'text'
      }
      // make request
      console.log(requestJSON);
      makeFlaskRequest(requestJSON, historicPowerGraph, historicPowerData)
    }
    updateHistoricPowerGraph(historicPowerGraph, historicPowerData)
    function resetHistoricPowerGraph(historicPowerGraph, historicPowerData){
      if (document.getElementById("datepicker_4").value == ''){
        startTime = Date.parse(new Date().toLocaleDateString('en-US')) / 1000
      } else {
        startTime = Date.parse(document.getElementById("datepicker_4").value) / 1000
      }
      endTime = startTime + 24 * 60 * 60
      updateHistoricPowerGraph(historicPowerGraph, historicPowerData)
    }
    $("#load_power").click(function(){
      resetHistoricPowerGraph(historicPowerGraph, historicPowerData)
    });
    $("#historic_chart_p").dblclick(function(){
      resetHistoricPowerGraph(historicPowerGraph, historicPowerData)
    });
    $("#download_all_power").click(function(){
      dataSize = 0;
      // create requestJSON
      let requestJSON = {
        startTime : startTime,
        endTime : endTime,
        dataName : "power",
        dataSize : dataSize,
        dataType : 'blob'
      }
      downloadAll(requestJSON);
    });
    $("#download_selected_power").click(function(){
      downloadSelected(historicPowerData);
    });
  });

  // Harmonische Spannung werden geklickt
  $("#H_U_h").click(function(){
    $("#Spannung_h, #Frequenz_h, #Strom_h, #Leistung_h, #Harmonische_I_h, .Inhalt_ist, .Inhalt_analy").hide();
    $("#Harmonische_U_h").show();
    changeColor(a="oben",b="aktiv", c="oben");
    clearTimers();
    let historicHarmonicUData = [[1,2],[3,4]];
    let historicHarmonicUGraph = simpleheat(document.getElementById('historic_heatmap_u'));
    historicHarmonicUGraph.max(Math.max(historicHarmonicUData))
    historicHarmonicUGraph.data(historicHarmonicUData)
    historicHarmonicUGraph.radius(1, 1);
    historicHarmonicUGraph.gradient({0.45: 'blue', 0.75: 'lime', 1: 'red'});
    historicHarmonicUGraph.draw()
  });

  // Harmonische Strom werden geklickt
  $("#H_I_h").click(function(){
    $("#Spannung_h, #Frequenz_h, #Strom_h, #Leistung_h, #Harmonische_U_h, .Inhalt_ist, .Inhalt_analy").hide();
    $("#Harmonische_I_h").show();
    changeColor(a="oben",b="aktiv", c="oben");
    clearTimers();
  });
  /* Analyse */

  // Spannung wurde geklickt
  $("#U_a").click(function(){
    $("#analyse_frequency, #analyse_THDu, #analyse_THDi, .Inhalt_ist, .Inhalt_hist").hide();
    $("#analyse_voltage").show();
    changeColor(a="oben",b="oben", c="aktiv");
    clearTimers();
    let dataName = 'voltage';
    let dataPhase = 1;
    let tableId = document.getElementById('AnalyseTabelleSpannung');
    updateFlaskRequestDeviationTable(tableId, dataPhase, dataName);
    $("#U_a_button_L1").click(function(){
      dataPhase = 1;
      updateFlaskRequestDeviationTable(tableId, dataPhase, dataName);
    });
    $("#U_a_button_L2").click(function(){
      dataPhase = 2;
      updateFlaskRequestDeviationTable(tableId, dataPhase, dataName);
    });
    $("#U_a_button_L3").click(function(){
      dataPhase = 3;
      updateFlaskRequestDeviationTable(tableId, dataPhase, dataName);
    });
  });

  // Frequenz wurde geklickt
  $("#f_a").click(function(){
    $("#analyse_voltage, #analyse_THDu, #analyse_THDi, .Inhalt_ist, .Inhalt_hist").hide();
    $("#analyse_frequency").show();
    changeColor(a="oben",b="oben", c="aktiv");
    clearTimers();
    let dataName = 'frequency';
    let dataPhase = 0;
    let tableId = document.getElementById('AnalyseTabelleFrequenz');
    updateFlaskRequestDeviationTable(tableId,dataPhase,dataName)
  });

  // THD U wurde geklickt
  $("#THD_U_a").click(function(){
    $("#analyse_frequency, #analyse_voltage, #analyse_THDi, .Inhalt_ist, .Inhalt_hist").hide();
    $("#analyse_THDu").show();
    changeColor(a="oben",b="oben", c="aktiv");
    clearTimers();
    let dataName = 'thdu';
    let dataPhase = 1;
    let tableId = document.getElementById('AnalyseTabelleTHDu');
    updateFlaskRequestDeviationTable(tableId, dataPhase, dataName);
    $("#THD_U_a_button_L1").click(function(){
      dataPhase = 1;
      updateFlaskRequestDeviationTable(tableId, dataPhase, dataName);
    });
    $("#THD_U_a_button_L2").click(function(){
      dataPhase = 2;
      updateFlaskRequestDeviationTable(tableId, dataPhase, dataName);
    });
    $("#THD_U_a_button_L3").click(function(){
      dataPhase = 3;
      updateFlaskRequestDeviationTable(tableId, dataPhase, dataName);
    });
  });

  // THD I wurde geklickt
  $("#THD_I_a").click(function(){
    $("#analyse_frequency, #analyse_THDu, #analyse_voltage, .Inhalt_ist, .Inhalt_hist").hide();
    $("#analyse_THDi").show();
    changeColor(a="oben",b="oben", c="aktiv");
    clearTimers();
    let dataName = 'thdi';
    let dataPhase = 1;
    let tableId = document.getElementById('AnalyseTabelleTHDi');
    updateFlaskRequestDeviationTable(tableId, dataPhase, dataName);
    $("#THD_I_a_button_L1").click(function(){
      dataPhase = 1;
      updateFlaskRequestDeviationTable(tableId, dataPhase, dataName);
    });
    $("#THD_I_a_button_L2").click(function(){
      dataPhase = 2;
      updateFlaskRequestDeviationTable(tableId, dataPhase, dataName);
    });
    $("#THD_I_a_button_L3").click(function(){
      dataPhase = 3;
      updateFlaskRequestDeviationTable(tableId, dataPhase, dataName);
    });
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
