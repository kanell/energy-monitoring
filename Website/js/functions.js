/* hide and show functions and clearinterval for the choices of the dropdown menu */

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
    if (Interval_I_t == 1) {window.clearInterval(Interval_I); Interval_I_t = 0;}
    if (Interval_f_t == 1) {window.clearInterval(Interval_f); Interval_f_t = 0;}
    if (Interval_U_t == 1) {window.clearInterval(Interval_U); Interval_U_t = 0;}
    if (Interval_L_t == 1) {window.clearInterval(Interval_L); Interval_L_t = 0;}
    // Hole gesuchte Werte ab
    currentValues();
  });

  // Spannung wird geklickt
  $("#U_i").click(function(){
    $("#Frequenz_i, #Strom_i, #Ubersicht_i, #Leistung_i, .Inhalt_hist, .Inhalt_analy").hide();
    $("#Spannung_i").show();
    changeColor(a="aktiv",b="oben", c="oben");
    if (Interval_I_t == 1) {window.clearInterval(Interval_I); Interval_I_t = 0;}
    if (Interval_f_t == 1) {window.clearInterval(Interval_f); Interval_f_t = 0;}
    if (Interval_Table_t == 1) {window.clearInterval(Interval_Table); Interval_Table_t = 0;}
    if (Interval_L_t == 1) {window.clearInterval(Interval_L); Interval_L_t = 0;}
    VoltageChart();
  });

  // Frequenz wird geklickt
  $("#f_i").click(function(){
    $("#Spannung_i, #Strom_i, #Ubersicht_i, #Leistung_i, .Inhalt_hist, .Inhalt_analy").hide();
    $("#Frequenz_i").show();
    changeColor(a="aktiv",b="oben", c="oben");
    if (Interval_I_t == 1) {window.clearInterval(Interval_I); Interval_I_t = 0;}
    if (Interval_U_t == 1) {window.clearInterval(Interval_U); Interval_U_t = 0;}
    if (Interval_Table_t == 1) {window.clearInterval(Interval_Table); Interval_Table_t = 0;}
    if (Interval_L_t == 1) {window.clearInterval(Interval_L); Interval_L_t = 0;}
    FrequencyChart();
  });

  // Strom wird geklickt
  $("#I_i").click(function(){
    $("#Frequenz_i, #Spannung_i, #Ubersicht_i, #Leistung_i, .Inhalt_hist, .Inhalt_analy").hide();
    $("#Strom_i").show();
    changeColor(a="aktiv",b="oben", c="oben");
    if (Interval_U_t == 1) {window.clearInterval(Interval_U); Interval_U_t = 0;}
    if (Interval_f_t == 1) {window.clearInterval(Interval_f); Interval_f_t = 0;}
    if (Interval_Table_t == 1) {window.clearInterval(Interval_Table); Interval_Table_t = 0;}
    if (Interval_L_t == 1) {window.clearInterval(Interval_L); Interval_L_t = 0;}
    CurrentChart();
  });

  // Leistung wird geklickt
  $("#L_i").click(function(){
    $("#Frequenz_i, #Spannung_i, #Ubersicht_i, #Strom_i, .Inhalt_hist, .Inhalt_analy").hide();
    $("#Leistung_i").show();
    changeColor(a="aktiv",b="oben", c="oben");
    if (Interval_I_t == 1) {window.clearInterval(Interval_I); Interval_I_t = 0;}
    if (Interval_f_t == 1) {window.clearInterval(Interval_f); Interval_f_t = 0;}
    if (Interval_Table_t == 1) {window.clearInterval(Interval_Table); Interval_Table_t = 0;}
    if (Interval_U_t == 1) {window.clearInterval(Interval_U); Interval_U_t = 0;}
    PowerChart();
    // PowerPolarChart();
  });
  /* Historische Werte */

  // Spannung wird geklickt
  $("#U_h").click(function(){
    $("#Frequenz_h, #Strom_h, #Leistung_h, #Harmonische_U_h, #Harmonische_I_h, .Inhalt_ist, .Inhalt_analy").hide();
    $("#Spannung_h").show();
    changeColor(a="oben",b="aktiv", c="oben");
    clearIntervalFunction();
    loadHistoricVoltageData();
    VoltageChart_h();
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
});

/* functions for the current values in the table */

function currentValues() {
  if ( Interval_Table_t == 1) {return;}
  else {
    getData();
    Interval_Table = window.setInterval(function (){
      Interval_Table_t = 1
      getData();
    }, 1000);
  }
}

// Get data function
function getData() {
  $.ajax({
    cache: false,
    url: "temp/json/livedata.json",
    dataType: "json",
    success: function(data) {
      var input = data
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
