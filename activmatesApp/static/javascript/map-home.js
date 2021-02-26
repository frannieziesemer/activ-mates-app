// Note: This example requires that you consent to location sharing when
// prompted by your browser. If you see the error "The Geolocation service
// failed.", it means you probably did not give permission for the browser to
// locate you.
let map, infoWindow;

function initMap() {
  map = new google.maps.Map(document.getElementById("map"), {
    center: { lat: -34.397, lng: 150.644 },
    zoom: 6,
  });
  infoWindow = new google.maps.InfoWindow();
  const locationButton = document.createElement("button");
  locationButton.textContent = "Pan to Current Location";
  locationButton.classList.add("custom-map-control-button");
  map.controls[google.maps.ControlPosition.TOP_CENTER].push(locationButton);

  google.maps.event.addListener(map, 'idle', function() {
    let center = map.getCenter();
    console.log('center point' + center)
    renderData(center);
  });


  locationButton.addEventListener("click", () => {
    // Try HTML5 geolocation.
    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(
        (position) => {
          const pos = {
            lat: position.coords.latitude,
            lng: position.coords.longitude,
          };
          infoWindow.setPosition(pos);
          infoWindow.setContent("Location found.");
          infoWindow.open(map);
          map.setCenter(pos);
        },
        () => {
          handleLocationError(true, infoWindow, map.getCenter());
        }
      );
    } else {
      // Browser doesn't support Geolocation
      handleLocationError(false, infoWindow, map.getCenter());
    }
  });
 
const renderData = (center) => {
  const params = {
    'lat': center.lat(),
    'lng': center.lng(),
    'radius': 5000000
  }
//add parameters to url
  const url = new URL('http://127.0.0.1:5000/api/get_activities');
  const searchParams = url.searchParams;
  for (const prop in params) {
    searchParams.set(encodeURIComponent(prop), encodeURIComponent(params[prop]));
  }
  url.search = searchParams.toString();
  const newUrl = url.toString() 
  

  loadJSON(newUrl);
  //loadJSON - send new url - also fetch 
}

//add idle event listener 
  //call clear markers function 
  //call querey markers function - 

}

const loadJSON = (url) => {
  let xhr = new XMLHttpRequest();
  xhr.open('GET', url, true);

  xhr.onload = function () {
    if (xhr.readyState === XMLHttpRequest.DONE && xhr.status === 200) {
      // Request finished. Do processing here 
      console.log('request finished', xhr.responseText)
    } else {
      console.log('request failed');
    }
  };
  //no data is being sent back 
  xhr.send(null);
}


function handleLocationError(browserHasGeolocation, infoWindow, pos) {
  infoWindow.setPosition(pos);
  infoWindow.setContent(
    browserHasGeolocation
      ? "Error: The Geolocation service failed."
      : "Error: Your browser doesn't support geolocation."
  );
  infoWindow.open(map);
}




// load the markers 
// call the api url = /api/get_activities
//add params to the api ?lat=111111&lng=22222






//tutorial - how to make json request
//https://developer.mozilla.org/en-US/docs/Learn/JavaScript/Objects/JSON

//info - edit map controls
// https://www.w3schools.com/graphics/google_maps_controls.asp 