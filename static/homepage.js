'use strict';
var Autocomplete;
      function initAutocomplete() {
        // Create the autocomplete object, restricting the search to geographical
        // location types.
        Autocomplete = new google.maps.places.Autocomplete(
            /** @type {!HTMLInputElement} */(document.getElementById('startpt')),
            {types: ['geocode']});

        console.log('hi')

        // When the user selects an address from the dropdown, populate the address
        // fields in the form.
        Autocomplete.addListener('place_changed', fillInAddress);
      }
      // place_changed - when user selects a place from the predictions attached, service fires a 'place_changed event' Can call getPlace() on the autocomplete object, to retrieve a PlaceResult object

      function fillInAddress() {
        // Get the place details from the autocomplete object.
        var place = Autocomplete.getPlace();

      console.log('are you working?')

      }

