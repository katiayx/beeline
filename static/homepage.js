'use strict';
// ##############################################################################
// adding autocomplete to form fields


var autocomplete;
var autocompleteWraps = ['startpt', 'location_a', 'location_b', 'location_c', 'location_d' ]

function initAutocomplete() {
  for (var i = 0; i < autocompleteWraps.length; i++) {
  // Create the autocomplete object, restricting the search to geographical
  // location types.
    autocomplete = new google.maps.places.Autocomplete(
        /** @type {!HTMLInputElement} */(document.getElementById(autocompleteWraps[i])),
        {types: ['geocode']});
  };
}

  

