
/* hide and show functions for the buttons of the left menu */
          
$(document).ready(function(){
    $("#U").click(function(){
        $("#Strom, #Ubersicht, #Leistung").hide();
    });
    $("#U").click(function(){
        $("#Spannung").show();
    });  
    $("#U").click(function(){                                               /* makes the content of "Spannung" visible for the first time click, necessery because it doesn't show up, if
                                                                            it's initially hidden by css's "display: none" command */
        document.getElementById("Spannung").style.visibility = "visible";   
    });  
     
});


$(document).ready(function(){
    $("#I").click(function(){
        $("#Spannung, #Ubersicht, #Leistung").hide();
    });
    $("#I").click(function(){
        $("#Strom").show();
    });
});


$(document).ready(function(){
    $("#Uber").click(function(){
        $("#Spannung, #Strom, #Leistung").hide();
    });
    $("#Uber").click(function(){
        $("#Ubersicht").show();
    });
});
              


$(document).ready(function(){
    $("#L").click(function(){
        $("#Spannung, #Ubersicht, #Strom").hide();
    });
    $("#L").click(function(){
        $("#Leistung").show();

    });
});



/*  functions for the current values in the table      */

$(document).ready(function(){

 

  window.intervalId = setInterval(function() {  
   
    $.ajax({
    cache: false,
    url: "http://localhost:8080/temp/json/alldata.json",
    dataType: "json",      
    success: function(data) {
     
     
      for (i=1; i <= 3; i++) {  
       var U = 806 + i*2;
       var I = 858 + i*2;
       var S = 882 + i*2;
       var P = 866 + i*2; 
       var Q = 874 + i*2;
       var THD_U = 834 + i*2;
       var THD_I = 906 + i*2;
       var f = 800                               
      
      document.getElementById("U" + i + "t").innerHTML =  data["port_" + U] ;
      document.getElementById("I" + i + "t").innerHTML =  data["port_" + I] ;
      document.getElementById("S" + i + "t").innerHTML =  data["port_" + S] ;
      document.getElementById("P" + i + "t").innerHTML =  data["port_" + P] ;
      document.getElementById("Q" + i + "t").innerHTML =  data["port_" + Q] ;
      document.getElementById("THD_U" + i + "t").innerHTML =  data["port_" + THD_U];
      document.getElementById("THD_I" + i + "t").innerHTML =  data["port_" + THD_I];  
      document.getElementById("ft").innerHTML =  data["port_" + f] ;                        
      };       
    }}); 
    }, 10000);                                                                     
  
});
    
   
    
/*     
$(document).ready(function(){

 

  $(function () {
  
   function update()  {  
   
       $.ajax({
    cache: false,
    url: "http://localhost:8080/temp/json/alldata.json",
    dataType: "json",      
    success: function(data) {
        
     
       
      for (i=1; i <= 3; i++) {  
       var U = 806 + i*2;
       var I = 858 + i*2;
       var S = 882 + i*2;
       var P = 866 + i*2; 
       var Q = 874 + i*2;
       var THD_U = 834 + i*2;
       var THD_I = 906 + i*2;
      /*var f = 800             /
      
      document.getElementById("U" + i + "t").innerHTML =  data["port_" + U] ;
      document.getElementById("I" + i + "t").innerHTML =  data["port_" + I] ;
      document.getElementById("S" + i + "t").innerHTML =  data["port_" + S] ;
      document.getElementById("P" + i + "t").innerHTML =  data["port_" + P] ;
      document.getElementById("Q" + i + "t").innerHTML =  data["port_" + Q] ;
      document.getElementById("THD_U" + i + "t").innerHTML =  data["port_" + THD_U];
      document.getElementById("THD_I" + i + "t").innerHTML =  data["port_" + THD_I];  
      /*document.getElementById("ft").innerHTML =  data["port_" + f] ;               
      };       
    }}); 
    
    }
    
   setInterval(update, 1000);
   update();
                                                                      
  
});
});
       
       
 */   