
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

