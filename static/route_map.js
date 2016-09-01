"use strict";
var directionsDisplay;
var directionsService;
var map;

function initialize() {
  directionsDisplay = new google.maps.DirectionsRenderer();
  directionsService = new google.maps.DirectionsService();
  var mapOptions = {
    zoom:4,
    center: {lat: 39.667913, lng: -99.268590}
  };
  map = new google.maps.Map(document.getElementById('map'), mapOptions);
  directionsDisplay.setMap(map);

  $(document).ready(displayRoute);
}

function displayRoute() {
  var start = $('#origin').val();
  var end = $('#destination').val();
  var waypoint_list = [];
  var waypoints = $('.stops');
  for (var i=0; i < waypoints.length; i++) {
      waypoint_list.push({
        location: waypoints[i].value,
        stopover: true
      });
    }
  directionsService.route({
    origin: start,
    destination: end,
    waypoints: waypoint_list,
    travelMode: 'DRIVING',
  }, function(result, status) {
    if (status == 'OK') {
      directionsDisplay.setDirections(result);
      var route = result.routes[0];
      var summaryPanel = document.getElementById('directions-panel');
      summaryPanel.innerHTML = '';
      // For each route, display summary information.
      for (var i = 0; i < route.legs.length; i++) {
        var routeSegment = i + 1;
        summaryPanel.innerHTML += '<b><b>SEGEMENT: ' + routeSegment +
          '</b><br>';
        summaryPanel.innerHTML += route.legs[i].start_address + '<br><em>to</em> ' +
          '<br>';
        summaryPanel.innerHTML += route.legs[i].end_address + '<br><br>';
      }
    } else {
      window.alert('Directions request failed due to ' + status);
    }
  });
}

console.log(directionsResult)

