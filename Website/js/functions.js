
/* hide and show functions for the buttons of the left menu */
          
$(document).ready(function(){
    $("#U").click(function(){
        $("#Strom, #Ubersicht, #Leistung").hide();
    });
    $("#U").click(function(){
        $("#Spannung").show();
    });  
    $("#U").click(function(){                                               
                                                                            
        VoltageChart();   
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
     $("#Uber").click(function(){                                               
                                                                            
        currentValues();   
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
var runValues;
function currentValues() {

 if (runValues == 1){
  return;
 }
getData();

  window.intervalId = setInterval(function() {  
   

getData();



    }, 10000); }
    
   
   function getData() {
   runValues = 1;

    $.ajax({
    cache: false,
    url: "http://localhost:8080/temp/json/alldata.json",
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