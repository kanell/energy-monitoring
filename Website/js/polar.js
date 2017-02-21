window.onload = function Leistung () {
var chart = AmCharts.makeChart("polar_chartdiv", {
  "type": "radar",
  "theme": "light",
  "dataProvider": [],
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
}