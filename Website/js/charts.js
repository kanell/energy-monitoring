/* Chart current Voltage */
var g;
 
     function VoltageChart () {

      

      var dataLength = 15;
      var csvData;



      $.ajax({
                    type: "GET",
                    cache: false,
                    url: "temp/csv/voltage.csv",
                    dataType: "text",
                    success: function (data) {
                       csvData = data;

                       VoltageGraph(csvData);
                       //alert("done!"+ csvData.getAllResponseHeaders()) - my fix makes this won't work...
                     }

                });




      function VoltageGraph () {
      //console.log(csvData);

     g = new Dygraph(document.getElementById("div_g"), csvData,
              {
                axis : {
                  x : {
                    valueFormatter: Dygraph.dateString_,
                    //valueParser: function(x) {return 1000*parteInt(x); },
                    ticker: Dygraph.dateTicker
                  }
                }
          });

      }



      Interval_U = window.setInterval(function() {
        runVoltage = 1;
         $.ajax({
                    type: "GET",
                    cache: false,
                    url: "temp/csv/voltage.csv",
                    dataType: "text",
                    success: function (data) {
                       csvData = data;

                       //VoltageGraph(csvData);
                       //alert("done!"+ csvData.getAllResponseHeaders()) - my fix makes this won't work...
                     }

                });

        g.updateOptions( { 'file': csvData } );

      }, 1000);
    }    
