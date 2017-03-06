/* Under Construction
    var jsonData;
     function PowerPolarChart () {
        
      $.ajax({
                    type: "GET",
                    cache: false,
                    url: "temp/json/livedata.json",
                    dataType: "json",
                    success: function (data) {
                       jsonData = data;

                       PowerPolarGraph(jsonData);
                       
                     }

                });



      function PowerPolarGraph () {
      //console.log(csvData);
      if ( Interval_L_P_t == 1) {return;}
      else {
      
      for (i=1; i <= 3; i++) {
       var S = 882 + i*2;
       var P = 866 + i*2;
       var Q = 874 + i*2;

        = jsonData["port_" + S] 

		var chart = AmCharts.makeChart("polar_chartdiv", {
		  "type": "radar",
		  "theme": "light",
		 "dataProvider": jsonData,
  		"valueAxes": [{
 		   "gridType": "circles",
 		   "minimum": 0
 		 }],

		  "polarScatter": {
		    "minimum": 0,
  		  "maximum": 359,
 		   "step": 1
 		 },
 		 "legend": {
 		   "position": "right"
  		},
 		 "graphs": [{
  		  "title": "Scheinleistung",
  		  "balloonText": "[[category]]: [[value]] m/s",
   		 "bullet": "round",
   		 "lineAlpha": 1,
   		 "series": [[0,0],[100,90]]
 		 }, {
  			  "title": "Wirkleistung",
   		 "balloonText": "[[category]]: [[value]] m/s",
  		  "bullet": "round",
   		 "lineAlpha": 1,
   		 "series": [[0,0],[90,89]]
 		 }, {
 		   "title": "Blindleistung",
  		  "balloonText": "[[category]]: [[value]] m/s",
  		  "bullet": "round",
  		  "lineAlpha": 1,
    
   		 "series": [[100,90],[90,89]]
 		 }],
 		 "export": {
  		  "enabled": true
 	 }
});

      


      Interval_L_P = window.setInterval(function() {
        Interval_L_P_t = 1;
        
         $.ajax({
                    type: "GET",
                    cache: false,
                    url: "temp/json/livedata.json",
                    dataType: "json",
                    success: function (data) {
                       jsonData = data;

                      }

                });

        g.updateOptions( { 'file': jsonData } );

      }, 1000);
    } }   }

    */