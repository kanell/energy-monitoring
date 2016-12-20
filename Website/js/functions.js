

          
$(document).ready(function(){
    $("#U").click(function(){
        $("#Strom, #Ubersicht").hide();
    });
    $("#U").click(function(){
        $("#Spannung").show();
    });
});


$(document).ready(function(){
    $("#I").click(function(){
        $("#Spannung, #Ubersicht").hide();
    });
    $("#I").click(function(){
        $("#Strom").show();
    });
});


$(document).ready(function(){
    $("#Uber").click(function(){
        $("#Spannung, #Strom").hide();
    });
    $("#Uber").click(function(){
        $("#Ubersicht").show();
    });
});


