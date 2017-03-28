/* function to append the Table in tab "Analyse" */
function Analyse(){
  var analyseResponseU1 = [{
    "Zeitpunkt" : "2017-02-16 13:32:31",
    "Wert" : "270",
    "Abweichung" : "13"},
    {"Zeitpunkt" : "2017-02-16 13:32:32",
    "Wert" : "273",
    "Abweichung" : "14"}
  ];
  // append to table
  AppendToTable(analyseResponseU1);
  // convert string to JSON
  function AppendToTable(){
    var trHTML = '';
    $.each(analyseResponseU1, function (i, item) {
      trHTML += '<tr><td>' + item.Zeitpunkt + '</td><td>' + item.Wert + '</td><td>' + item.Abweichung + '</td></tr>';
    });
    $('#AnalyseTabelleU1').append(trHTML);
  }
}
