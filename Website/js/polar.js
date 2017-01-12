/**
 * Create the chart
 * Uses amCharts Polar Scatter plugin:
 * https://github.com/amcharts/tools/tree/master/polarScatter
 */
window.onload = function Leistung () {
var chart = AmCharts.makeChart("chartdiv", {
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
    "title": "Trial #1",
    "balloonText": "[[category]]: [[value]] m/s",
    "bullet": "round",
    "lineAlpha": 1,
    "series": [[0,0],[100,90]]
  }, {
    "title": "Trial #2",
    "balloonText": "[[category]]: [[value]] m/s",
    "bullet": "round",
    "lineAlpha": 1,
    "series": [[100,90],[90,89]]
  }, {
    "title": "Trial #3",
    "balloonText": "[[category]]: [[value]] m/s",
    "bullet": "round",
    "lineAlpha": 1,
    "series": [[0,0],[90,89]]
  }],
  "export": {
    "enabled": true
  }
});
}