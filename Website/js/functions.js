

          
$(document).ready(function(){
    $("#U").click(function(){
        $("#Strom, #Ubersicht, #Leistung").hide();
    });
    $("#U").click(function(){
        $("#Spannung").show();
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