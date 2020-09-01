// ---------------------------------------------------------------------------
// log.js
// 
// Author: Kevin McAndrew
// Created: 14 Aug 2020
// ---------------------------------------------------------------------------

// ---------------------------------------------------------------------------
// Chart objects
// ---------------------------------------------------------------------------
var chartT = new Highcharts.Chart({
  chart: { 
    renderTo: 'log_card',
    backgroundColor: "#f8f8f8",
    height: 200
    },
  title: { text: 'Test Chart' },
  series: [{
    showInLegend: false,
    data: []
  }],
  plotOptions: {
    line: { animation: false,
    dataLabels: { enabled: true }
    },
    series: { color: '#059e8a' }
  },
  xAxis: { type: 'datetime',
    dateTimeLabelFormats: { second: '%H:%M:%S' }
  },
  yAxis: {
    title: { text: 'y axis' }
    //title: { text: 'Temperature (Fahrenheit)' }
  },
  credits: { enabled: false }
  });

// ---------------------------------------------------------------------------
// Web sockets
// ---------------------------------------------------------------------------
function testWebSocket()
{
  var wsUri       = "ws://" + window.location.hostname;
  console.log("Connection to " + wsUri + "...");
  websocket       = new WebSocket(wsUri);
  websocket.onopen  = function(evt) { onOpen  (evt) };
  websocket.onmessage = function(evt) { onMessage (evt) };
  websocket.onclose   = function(evt) { onClose   (evt) };
  websocket.onerror   = function(evt) { onError   (evt) };
}
// Open
// - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
function onOpen(evt)
{
  console.log("Websocket disconnected :(");
}
// Close
// - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
function onClose(evt)
{
  console.log("Websocket closed");
}
// Error
// - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
function onError(evt)
{
  console.log("Websocket error");
}
// Receive Message
// - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
function onMessage(evt)
{
  var x = (new Date()).getTime(),
    y = parseFloat(evt.data);
  if(chartT.series[0].data.length > 20) {
    chartT.series[0].addPoint([x, y], true, true, true);
  } else {
    chartT.series[0].addPoint([x, y], true, false, true);
  }
}
// Timer Interval
// - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
setInterval(function () {
  if(websocket.readyState == 1){
    websocket.send("Need update : " + (new Date()).getTime());
  }
}, 1000 ) ;

window.addEventListener("load", testWebSocket, false);