'use strict';
var map;
function initMap() {
    var markerArray = []
    
    //instantiate a directions service
    var directionsService = new google.maps.DirectionsService;
    //create a map object and center on USA
    var map = new google.maps.Map(document.getElementById('map'), {
      center: {lat: 39.667913, lng: -99.268590},
      zoom: 4    
    });
    //Create a renderer for directions and bind it to the map.
    var directionsDisplay = new google.maps.DirectionsRenderer({map: map});
    
    //Instantiate an info window to hold step text.
    var stepDisplay = new google.maps.InfoWindow;

    // Display the route between the initial start and end selections.
    calculateAndDisplayRoute(
        directionsDisplay, directionsService, markerArray, stepDisplay, map);
    
    // // Listen to change events from the start and end lists.
    // var onChangeHandler = function() {
    //   calculateAndDisplayRoute(
    //       directionsDisplay, directionsService, markerArray, stepDisplay, map);
    // };
    // document.getElementById('start').addEventListener('change', onChangeHandler);
    // document.getElementById('end').addEventListener('change', onChangeHandler);
}

function calculateAndDisplayRoute(directionsDisplay, directionsService,
markerArray, map) {
// First, remove any existing markers from the map.
    
    for (var i = 0; i < markerArray.length; i++) {
            markerArray[i].setMap(null);    
    }

var origin;
var waypoints;
var destination;

function getStops(evt) {
    evt.preventDefault():
    
    .get('/stops.json', calculateAndDisplayRoute,
        //JSON looks like:
        // '{
        //   'oakland':
        //      ['san francisco'
        //       'fremont'
        //       'san mateo']
        //  }'
        origin = {
            Object.keys(stops_d);
        };

        destination = {
            stops_d[key];
        };

        var waypoints = {
            stops_d[key][stops_d[key].length - 1];
        };
        // Retrieve the start and end locations and create a DirectionsRequest
    directionsService.route({
      origin: origin,
      destination: destination,
      waypoints: waypoints,  
      travelMode: 'DRIVING'
    }, function(response, status) {
          // Route the directions and pass the response to a function to create
          // markers for each step.
          if (status === 'OK') {
            directionsDisplay.setDirections(response);
            showSteps(response, markerArray, stepDisplay, map);
          } else {
            window.alert('Directions request failed due to ' + status);
          }
        });
}

function showSteps(directionResult, markerArray, stepDisplay, map) {
// For each step, place a marker, and add the text to the marker's infowindow.
// Also attach the marker to an array so we can keep track of it and remove it
// when calculating new routes.
    var myRoute = directionResult.routes[0].legs[0];
    for (var i = 0; i < myRoute.steps.length; i++) {
      var marker = markerArray[i] = markerArray[i] || new google.maps.Marker;
      marker.setMap(map);
      marker.setPosition(myRoute.steps[i].start_location);
      attachInstructionText(
          stepDisplay, marker, myRoute.steps[i].instructions, map);
    }
}

// function attachInstructionText(stepDisplay, marker, text, map) {
//     google.maps.event.addListener(marker, 'click', function() {
//       // Open an info window when the marker is clicked on, containing the text
//       // of the step.
//       stepDisplay.setContent(text);
//       stepDisplay.open(map, marker);
//     });
// }

  