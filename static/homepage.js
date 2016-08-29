'use strict';

// function getInput(evt) {
//   evt.preventDefault();

//   var locations = {
//     'loc': $('#user_input_form').serialize();
    
//   };

//   $.post('/distance', locations, function(response) {
//       if (response.d == true) {
//         console.log('Successfully passed to server')
//     };
//   });
// }

“”“form.serialize() only capturing first input

$('input#user_input_form').on("submit", getInput)


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
   



