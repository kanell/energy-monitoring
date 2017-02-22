
/* hide and show functions for the buttons of the dropdown menu */


/* "Aktuelle Werte" */

$(document).ready(function(){

    $("#U_i").click(function(){


    $("#Strom_i, #Ubersicht_i, #Leistung_i, .Inhalt_hist, .Inhalt_analy").hide();

    $("#Spannung_i").show();

    changeColor(a="aktiv",b="oben", c="oben");

    VoltageChart();

    });





    $("#I_i").click(function(){
        $("#Spannung_i, #Ubersicht_i, #Leistung_i, .Inhalt_hist, .Inhalt_analy").hide();

        $("#Strom_i").show();

        changeColor(a="aktiv",b="oben", c="oben");

      });




    $("#Uber_i").click(function(){
        $("#Spannung_i, #Strom_i, #Leistung_i, .Inhalt_hist, .Inhalt_analy").hide();

        $("#Ubersicht_i").show();

        changeColor(a="aktiv",b="oben", c="oben");


        currentValues();

    });





    $("#L_i").click(function(){
        $("#Spannung_i, #Ubersicht_i, #Strom_i, .Inhalt_hist, .Inhalt_analy").hide();

        $("#Leistung_i").show();

        changeColor(a="aktiv",b="oben", c="oben");

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
var runValues;
function currentValues() {

 if (runValues == 1){
  return;
 }

 else {
getData();

  window.intervalId = setInterval(function() {


getData();



    }, 10000); } }


   function getData() {
   runValues = 1;

    $.ajax({
    cache: false,
    url: "temp/json/alldata.json",
    dataType: "json",

    success: function(data) {

     var input = data
     console.log(input)
      for (i=1; i <= 3; i++) {
       var U = 806 + i*2;
       console.log(U);
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
    }




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
