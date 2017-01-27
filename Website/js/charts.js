/* Chart current Voltage */

 
     $(document).ready(function () {
      var data = []; 
      var dataLength = 15;
      var t = new Date();
      for (var i = 10; i >= 0; i--) {
        var x = new Date(t.getTime() - i * 1000);
        var z = 1.1;
        data.push([x, Math.random(),z]);
       
      }

      var g = new Dygraph("div_g", data,
                          {
                            
                            drawPoints: true,
                            showRoller: false,
                            valueRange: [0.0, 1.2],
                            labels: ['Time', 'Random','Linie']
                          });
      // It sucks that these things aren't objects, and we need to store state in window.
     window.intervalId = setInterval(function() {
        var x = new Date();  // current time
        var y = Math.random();
        var z = 1.1;
        data.push([x, y, z]);
        g.updateOptions( { 'file': data } );
         if (data.length > dataLength) {
        data.shift();
        };
      }, 1000);      
    }            
);       /*


 $(document).ready(function () {
         var dataLenght = 15;
         var r = "date, values,line max,line min\n";
         var t = new Date();   
         
          for (var i=1; i<=10; i++) {
                r += new Date(t.getTime() - i * 1000);
                r += "," + Math.random();
                r += "," + 1.1;
                r += "," + 0.9;
                r += "\n";
                }    
      
      
      var g = new Dygraph(
              "div_g", r,
              {
                
                series: {
                  'values': {
                    strokeWidth: 0.0,
                    drawPoints: true,
                    pointSize: 4,
                    highlightCircleSize: 6
                  },
                  'line max': {
                    strokeWidth: 1.0,
                    drawPoints: true,
                    pointSize: 1.5
                  },
                  'line min': {
                    strokeWidth: 3,
                    highlightCircleSize: 10
                  }
                }
              }
          );  
          
          window.intervalId = setInterval(function() {
       
         
          r += new Date();
          r += "," + Math.random();
          r += "," + 1.1;
          r += "," + 0.9;
          r += "\n";
          
          
      
          g.updateOptions( { 'file': r } );  
          
          
              if (r.length > dataLength) {
              r.shift();
              };        
              
         }, 1000);
    }
<<<<<<< HEAD
=======
); */
>>>>>>> 64754c3f9f6798386aee4ce8efb9c188a05db046
