/* Chart current Voltage */
var g;
var csvData;
var Interval_U_t;
var Interval_I_t;
var Interval_f_t;
var Interval_Table_t;
var Interval_L_t;


function VoltageChart () {
  $.ajax({
    type: "GET",
    cache: false,
    url: "temp/csv/voltage.csv",
    dataType: "text",
    success: function (data) {
      csvData = data;
      VoltageGraph(csvData);
    }
  });
  // Set graph
  function VoltageGraph () {
    //console.log(csvData);
    if ( Interval_U_t == 1) {return;}
    else {
      g = new Dygraph(document.getElementById("div_U"), csvData,{
        xValueParser : function(x) {return 1000 * parseFloat(x);},
        axes : {
          x : {
              valueFormatter : function(x) {return Dygraph.dateString_(x,0);},
              axisLabelFormatter : Dygraph.dateAxisLabelFormatter,
              ticker: Dygraph.dateTicker
          }
        }
      });
      // set Interval
      Interval_U = window.setInterval(function() {
        Interval_U_t = 1;
        $.ajax({
                    type: "GET",
                    cache: false,
                    url: "temp/csv/voltage.csv",
                    dataType: "text",
                    success: function (data) {
                       csvData = data;

                      }

                });

        g.updateOptions( { 'file': csvData } );

      }, 1000);
    } }   }



     function CurrentChart () {


      $.ajax({
                    type: "GET",
                    cache: false,
                    url: "temp/csv/current.csv",
                    dataType: "text",
                    success: function (data) {
                       csvData = data;

                       CurrentGraph(csvData);

                     }

                });




      function CurrentGraph () {
      //console.log(csvData);
      if ( Interval_I_t == 1) {return;}
      else {
     g = new Dygraph(document.getElementById("div_I"), csvData,
              {
		xValueParser : function(x) {return 1000 * parseFloat(x);},
                axes : {
                  	x : {
                    		valueFormatter: function(x) {return Dygraph.dateString_(x,0);},
                    		axisLabelFormatter : Dygraph.dateAxisLabelFormatter,
                    		ticker: Dygraph.dateTicker
                  	}
                }
          });





      Interval_I = window.setInterval(function() {
       Interval_I_t = 1
         $.ajax({
                    type: "GET",
                    cache: false,
                    url: "temp/csv/current.csv",
                    dataType: "text",
                    success: function (data) {
                       csvData = data;


                     }

                });

        g.updateOptions( { 'file': csvData } );

      }, 1000);
    }  }}





         function PowerChart () {


      $.ajax({
                    type: "GET",
                    cache: false,
                    url: "temp/csv/power.csv",
                    dataType: "text",
                    success: function (data) {
                       csvData = data;

                       PowerGraph(csvData);

                     }

                });




      function PowerGraph () {
      //console.log(csvData);
      if ( Interval_L_t == 1) {return;}
      else {
     g = new Dygraph(document.getElementById("div_L"), csvData,
              {
                xValueParser : function(x) {return 1000 * parseFloat(x);},
		axes : {
                  	x : {
                    		valueFormatter: function(x) {return Dygraph.dateString_(x,0);},
                    		axisLabelFormatter : Dygraph.dateAxisLabelFormatter,
                    		ticker: Dygraph.dateTicker
                  	}
                }
          });





      Interval_L = window.setInterval(function() {
        Interval_L_t = 1
         $.ajax({
                    type: "GET",
                    cache: false,
                    url: "temp/csv/power.csv",
                    dataType: "text",
                    success: function (data) {
                       csvData = data;


                     }

                });

        g.updateOptions( { 'file': csvData } );

      }, 1000);
    } }}



function FrequencyChart () {

      $.ajax({
                    type: "GET",
                    cache: false,
                    url: "temp/csv/frequency.csv",
                    dataType: "text",
                    success: function (data) {
                       csvData = data;

                       FrequencyGraph(csvData);

                     }

                });



      function FrequencyGraph () {
      //console.log(csvData);
      if ( Interval_U_t == 1) {return;}
      else {
     g = new Dygraph(document.getElementById("div_f"), csvData,
              {
             	digitsAfterDecimal : 4,
		xValueParser: function(x) {return 1000 * parseFloat(x);},
                axes : {
                 x: {
                    valueFormatter: function(x) {return Dygraph.dateString_(x,0);},
                    axisLabelFormatter: Dygraph.dateAxisLabelFormatter,
                    ticker: Dygraph.dateTicker
                   }
                }

          });





      Interval_f = window.setInterval(function() {
        Interval_f_t = 1
         $.ajax({
                    type: "GET",
                    cache: false,
                    url: "temp/csv/frequency.csv",
                    dataType: "text",
                    success: function (data) {
                       csvData = data;

                      }

                });

        g.updateOptions( { 'file': csvData } );

      }, 1000);
    }  }}
