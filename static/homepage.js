'use strict';

function getInput(evt) {
  evt.preventDefault();

  var locations = {
    'loc': $('#user_input_form').serializeArray();
  };

  $.post('/distance', locations, function(response) {
      if (response.d == true) {
        console.log('Successfully passed to server')
    };
  };
}

$('#user_input_form').on("submit", getInput)



var autocomplete;
var autocompleteWraps = ['startpt', 'location_a', 'location_b', 'location_c', 'location_d' ]

// not yet tested
      function initAutocomplete() {
        for (var i = 0; i < autocompleteWraps.length; i++) {
        // Create the autocomplete object, restricting the search to geographical
        // location types.
          autocomplete = new google.maps.places.Autocomplete(
              /** @type {!HTMLInputElement} */(document.getElementById(autocompleteWraps[i])),
              {types: ['geocode']});

          // When the user selects an address from the dropdown, populate the address
          // fields in the form.
          autocompleteWraps[i].addListener('place_changed', function (){
            var place = autocompleteWraps[i].getPlace();
          });
        };
      }
   



