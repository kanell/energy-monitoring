
/* hide and show functions and clearinterval for the choices of the dropdown menu */


/* "Aktuelle Werte" */

$(document).ready(function(){




   $("#Uber_i").click(function(){
        $("#Frequenz_i, #Spannung_i, #Strom_i, #Leistung_i, .Inhalt_hist, .Inhalt_analy").hide();

        $("#Ubersicht_i").show();

        changeColor(a="aktiv",b="oben", c="oben");

        if (Interval_I_t == 1) {window.clearInterval(Interval_I); Interval_I_t = 0;}
        if (Interval_f_t == 1) {window.clearInterval(Interval_f); Interval_f_t = 0;}
        if (Interval_U_t == 1) {window.clearInterval(Interval_U); Interval_U_t = 0;}
        if (Interval_L_t == 1) {window.clearInterval(Interval_L); Interval_L_t = 0;}

        currentValues();

    });



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




   





    $("#L_i").click(function(){
        $("#Frequenz_i, #Spannung_i, #Ubersicht_i, #Strom_i, .Inhalt_hist, .Inhalt_analy").hide();

        $("#Leistung_i").show();

        changeColor(a="aktiv",b="oben", c="oben");

        if (Interval_I_t == 1) {window.clearInterval(Interval_I); Interval_I_t = 0;}
        if (Interval_f_t == 1) {window.clearInterval(Interval_f); Interval_f_t = 0;}
        if (Interval_Table_t == 1) {window.clearInterval(Interval_Table); Interval_Table_t = 0;}
        if (Interval_U_t == 1) {window.clearInterval(Interval_U); Interval_U_t = 0;}

        PowerChart();

        });
});

/*Historische Werte*/

$(document).ready(function(){

    $("#U_h").click(function(){

              $("#Frequenz_h, #Strom_h, #Leistung_h, #Harmonische_U_h, #Harmonische_I_h, .Inhalt_ist, .Inhalt_analy").hide();


        $("#Spannung_h").show();

        changeColor(a="oben",b="aktiv", c="oben");


        Historie();

    });

     $("#f_h").click(function(){

              $("#Spannung_h, #Strom_h, #Leistung_h, #Harmonische_U_h, #Harmonische_I_h, .Inhalt_ist, .Inhalt_analy").hide();

        $("#Frequenz_h").show();

        changeColor(a="oben",b="aktiv", c="oben");

    });

     $("#I_h").click(function(){

              $("#Spannung_h, #Frequenz_h, #Leistung_h, #Harmonische_U_h, #Harmonische_I_h, .Inhalt_ist, .Inhalt_analy").hide();

        $("#Strom_h").show();

        changeColor(a="oben",b="aktiv", c="oben");

    });

     $("#L_h").click(function(){

              $("#Spannung_h, #Frequenz_h, #Strom_h, #Harmonische_U_h, #Harmonische_I_h, .Inhalt_ist, .Inhalt_analy").hide();

        $("#Leistung_h").show();

        changeColor(a="oben",b="aktiv", c="oben");

    });

     $("#H_U_h").click(function(){

              $("#Spannung_h, #Frequenz_h, #Strom_h, #Leistung_h, #Harmonische_I_h, .Inhalt_ist, .Inhalt_analy").hide();

        $("#Harmonische_U_h").show();

        changeColor(a="oben",b="aktiv", c="oben");

    });

     $("#H_I_h").click(function(){

              $("#Spannung_h, #Frequenz_h, #Strom_h, #Leistung_h, #Harmonische_U_h, .Inhalt_ist, .Inhalt_analy").hide();

        $("#Harmonische_I_h").show();

        changeColor(a="oben",b="aktiv", c="oben");

    });
});

/* Analyse */

$(document).ready(function(){

        $("#U1_a").click(function(){

           $("#Spannung_2_a, #Spannung_3_a, #Frequenz_a, #Harmonische_U_a, #Harmonische_I_a, .Inhalt_ist, .Inhalt_hist").hide();

           $("#Spannung_1_a").show();

          changeColor(a="oben",b="oben", c="aktiv");

          Analyse();

        });

        $("#U2_a").click(function(){

           $("#Spannung_1_a, #Spannung_3_a, #Frequenz_a, #Harmonische_U_a, #Harmonische_I_a, .Inhalt_ist, .Inhalt_hist").hide();

           $("#Spannung_2_a").show();

          changeColor(a="oben",b="oben", c="aktiv");

        });

        $("#U3_a").click(function(){

           $("#Spannung_1_a, #Spannung_2_a, #Frequenz_a, #Harmonische_U_a, #Harmonische_I_a, .Inhalt_ist, .Inhalt_hist").hide();

           $("#Spannung_3_a").show();

          changeColor(a="oben",b="oben", c="aktiv");

        });

        $("#f_a").click(function(){

           $("#Spannung_1_a, #Spannung_2_a, #Spannung_3_a, #Harmonische_U_a, #Harmonische_I_a, .Inhalt_ist, .Inhalt_hist").hide();

           $("#Frequenz_a").show();

          changeColor(a="oben",b="oben", c="aktiv");

        });


        $("#THD_U_a").click(function(){

           $("#Spannung_1_a, #Spannung_2_a, #Spannung_3_a, #Frequenz_a, #Harmonische_I_a, .Inhalt_ist, .Inhalt_hist").hide();

           $("#Harmonische_U_a").show();

          changeColor(a="oben",b="oben", c="aktiv");

        });



        $("#THD_I_a").click(function(){

           $("#Spannung_1_a, #Spannung_2_a, #Spannung_3_a, #Frequenz_a, #Harmonische_U_a, .Inhalt_ist, .Inhalt_hist").hide();

           $("#Harmonische_I_a").show();

          changeColor(a="oben",b="oben", c="aktiv");

        });

});


/*  functions for the current values in the table      */

function currentValues() {
if ( Interval_Table_t == 1) {return;}
      else {
getData();

  Interval_Table = window.setInterval(function (){
    Interval_Table_t = 1


    getData();

    }, 1000); 


   function getData() {
   

    $.ajax({
    cache: false,
    url: "temp/json/livedata.json",
    dataType: "json",

    success: function(data) {

     var input = data
     //console.log(input)
      for (i=1; i <= 3; i++) {
       var U = 806 + i*2;
       var I = 858 + i*2;
       var S = 882 + i*2;
       var P = 866 + i*2;
       var Q = 874 + i*2;
       var THD_U = 834 + i*2;
       var THD_I = 906 + i*2;
       var f = 800

      document.getElementById("U" + i + "t").innerHTML =  input["port_" + U] ;
      document.getElementById("I" + i + "t").innerHTML =  input["port_" + I] ;
      document.getElementById("S" + i + "t").innerHTML =  input["port_" + S] ;
      document.getElementById("P" + i + "t").innerHTML =  input["port_" + P] ;
      document.getElementById("Q" + i + "t").innerHTML =  input["port_" + Q] ;
      document.getElementById("THD_U" + i + "t").innerHTML =  input["port_" + THD_U];
      document.getElementById("THD_I" + i + "t").innerHTML =  input["port_" + THD_I];
      document.getElementById("ft").innerHTML =  input["port_" + f] ;
      };
    }});
    }}}




/*
$(function() {
    $.each(analyseResponseU1, function(i, item) {
        var $tr = $('<tr>').append(
            $('<td>').text(item.Zeitpunkt),
            $('<td>').text(item.Wert),
            $('<td>').text(item.Abweichung)
        ); $tr.appendTo('#AnalyseTabelleU1');
        console.log($tr.wrap('<p>').html());
    });
}); */


/* Changes the Color of the selected Tab */
function changeColor() {


    document.getElementById("aktuell").className = a;
    document.getElementById("historisch").className = b;
    document.getElementById("analysiert").className = c;

  }
