// Note: This example requires that you consent to location sharing when
// prompted by your browser. If you see the error "The Geolocation service
// failed.", it means you probably did not give permission for the browser to
// locate you.
let map, infoWindow, markers;

function initMap() {
  map = new google.maps.Map(document.getElementById("map"), {
    center: { lat: 52.5200, lng: 13.4050 }, 
    zoom: 10,
  });
  infoWindow = new google.maps.InfoWindow();
  const locationButton = document.createElement("button");
  locationButton.textContent = "Pan to Current Location";
  locationButton.classList.add("custom-map-control-button");
  map.controls[google.maps.ControlPosition.TOP_CENTER].push(locationButton);

  google.maps.event.addListener(map, 'idle', function() {
    let center = map.getCenter();
    //let zoom = map.getZoom();
    
    renderData(center);
  });
// event listene for pan to current location
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

  clearMarkers();

  const params = {
    'lat': center.lat(),
    'lng': center.lng(),
    'radius': 6000
  }
//add parameters to url
  const url = new URL('http://127.0.0.1:5000/api/get_activities');
  const searchParams = url.searchParams;
  for (const prop in params) {
    searchParams.set(encodeURIComponent(prop), encodeURIComponent(params[prop]));
  }
  url.search = searchParams.toString();
  const newUrl = url.toString() 
  // is it better to have a callback ? 
  //- yes because now all of the functions to render the data are being called inside RenderData function -
  // clearMarkers - addMarkers
  loadJSON(newUrl, function parseJSON(response) {
    activities = JSON.parse(response);
    //JSPN parse response data 
    //call place markers on map function - passing JSON response in
    addMarkersToMap(activities);
  }); 
}
}
//https://developer.mozilla.org/en-US/docs/Web/API/XMLHttpRequest/send#example_get
const loadJSON = (url, parseJSON) => {
  let xhr = new XMLHttpRequest();
  // 'open' the http request
  console.log(url);
  xhr.open('GET', url, true);
  // function handles what to do when the data is loaded / handles a failed request 
  xhr.onload = function () {
    if (xhr.readyState === XMLHttpRequest.DONE && xhr.status === 200) {
      // Request finished. Do processing here  //response text = string 
      response = xhr.responseText;
      parseJSON(response);
    } else {
      console.log('request failed');
      //TODO: a more meaningful response on failed data 
    }
  };
  //no data is being sent back becasue we want to fetch
  xhr.send(null);
}




function addMarkersToMap(activities) {
  //markers need to be stored in an array so I can access and manipulate without overwriting on forEach loop 
  markers = [];

//maybe it is better to use map here.. 
  activities.forEach(activity => {
    const latLng = { lat: activity.location.lat, lng: activity.location.lng }
    const marker =  new google.maps.Marker({
      position: latLng,
      map,
      icon: 'http://127.0.0.1:5000/static/images/icons/run.svg',
      title: activity.description,
    });
    
    marker.addListener('click', () => {
      displayActivity(activities);
    })
    
    
    //add event listener to each marker 

  });
  //TODO add click functionality to marker - to display activity info when clicked 
}

function clearMarkers() {
  if(markers) {
    markers.forEach(marker => marker.setMap(null));
  }


}

function displayActivity (activities) {
  console.log(activities)
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