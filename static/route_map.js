'use strict';
var directionsService;
var directionsDisplay;
var map;

function initMap() {
    // Instantiate a directions service.
    directionsService = new google.maps.DirectionsService();
    // Create a renderer for directions and bind it to the map.
    directionsDisplay = new google.maps.DirectionsRenderer();
    //create a map object and center on US
    map = new google.maps.Map(document.getElementById('map'), {
        center: {
            lat: 39.667913,
            lng: -99.268590
        },
        zoom: 4
    });

    directionsDisplay.setMap(map);
    directionsDisplay.setPanel(document.getElementById('directions-panel'));

    calcRoute(directionsDisplay, directionsService);
}

function calcRoute(directionsService, directionsDisplay) {
    var waypts = [];
    var waypoints = $('#waypts').val();
    for (var i = 0; i < waypoints.length; i++) {
        waypts.push({
            location: waypoints[i].value,
            stopover: true
        });
    };
    directionsService.route({
        origin: $('#origin').val(),
        destination: $('#destination').val(),
        waypoints: waypts,
        travelMode: 'DRIVING'
    }, function(result, status) {
        if (status == 'OK') {
            directionsDisplay.setDirections(result);
        } else {
            alert('Directions request failed due to ' + status);
        }
    });
}