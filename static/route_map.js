'use strict';
var map;
var directionsService = new google.maps.DirectionsService();
var directionsDisplay = new google.maps.DirectionsRenderer();
var origin;
var waypoints;
var destination;
var stops_d;


function initMap() {
    //create a map object and center on US
    map = new google.maps.Map(document.getElementById('map'), {
      center: {lat: 39.667913, lng: -99.268590},
      zoom: 4    
    });
     directionsDisplay.setMap(map);
}




function getStops() {
    $.get('/distance', 
      function(stops_d) {
        //JSON looks like:
        // '{
        //   'oakland':
        //      ['san francisco'
        //       'fremont'
        //       'san mateo']
        //  }'

        console.log(stops_d);

    origin = {
      Object.keys(stops_d)[0];
    }; 
    // returns 'string'

    destination = {
      stops_d[origin].slice(-1);
    };

    waypoints = {
      stops_d[origin].slice(0, -1);
     };
    });

}

function calcRoute() {
  getStops();
  var request = {
      origin: origin,
      destination: destination,
      waypoints: waypoints,  
      travelMode: 'DRIVING'
    };
    directionsService.route(request, function(result, status) {
    if (status == 'OK') {
      directionsDisplay.setDirections(result);
    }
  });
}

calcRoute();
  