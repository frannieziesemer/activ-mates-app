console.log("it works ");

let placeSearch, autocomplete;

function initAutocomplete() {
  console.log("autocomplete");
  // Create the autocomplete object, restricting the search to geographical
  // location types.
  autocomplete = new google.maps.places.Autocomplete(
    /** @type {!HTMLInputElement} */ (document.getElementById("autocomplete")),
    { types: ["geocode"] }
  );

  // When the user selects an address from the dropdown, populate the address
  // fields in the form.
  autocomplete.addListener("place_changed", onPlaceChanged);
}

function onPlaceChanged() {
  let place = autocomplete.getPlace();
  console.log(place);
  console.log(place.formatted_address);
  console.log(place.geometry.location.lat());
  console.log(place.geometry.location.lng());

  if (!place.geometry) {
    //User did not select a predicition; reset the input field
    document.getElementById("autocomplete").placeholder = "Enter your address";
  } else {
    //Display detials about the valid place
    document.getElementById("details").innerHTML = place.formatted_address;
    document.getElementById("lat").value = place.geometry.location.lat();
    document.getElementById("lng").value = place.geometry.location.lng();
    document.getElementById("address").value = place.formatted_address;
  }
}
// Bias the autocomplete object to the user's geographical location,
// as supplied by the browser's 'navigator.geolocation' object.
function geolocate() {
  if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(function (position) {
      var geolocation = {
        lat: position.coords.latitude,
        lng: position.coords.longitude,
      };
      var circle = new google.maps.Circle({
        center: geolocation,
        radius: position.coords.accuracy,
      });
      autocomplete.setBounds(circle.getBounds());
    });
  }
}

google.maps.event.addDomListener(window, "load", initAutocomplete);
