// Note: This example requires that you consent to location sharing when
// prompted by your browser. If you see the error "The Geolocation service
// failed.", it means you probably did not give permission for the browser to
// locate you.
let map, infoWindow, markers;

function initMap() {
  map = new google.maps.Map(document.getElementById("map"), {
    center: { lat: 52.52, lng: 13.405 },
    zoom: 10,
    streetViewControl: false,
    mapTypeControl: false,
    scaleControl: false,
    rotateControl: false,
    fullscreenControl: false,
  });

  infoWindow = new google.maps.InfoWindow();
  const locationButton = document.createElement("button");
  locationButton.textContent = "Pan to Current Location";
  locationButton.classList.add("custom-map-control-button");
  map.controls[google.maps.ControlPosition.TOP_CENTER].push(locationButton);

  google.maps.event.addListener(map, "idle", function () {
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
      lat: center.lat(),
      lng: center.lng(),
      radius: 6000,
    };
    //add parameters to url
    const url = new URL("http://127.0.0.1:5000/api/get_activities");
    const searchParams = url.searchParams;
    for (const prop in params) {
      searchParams.set(
        encodeURIComponent(prop),
        encodeURIComponent(params[prop])
      );
    }
    url.search = searchParams.toString();
    const newUrl = url.toString();
    // is it better to have a callback ?
    //- yes because now all of the functions to render the data are being called inside RenderData function -
    // clearMarkers - addMarkers
    loadJSON(newUrl, function parseJSON(response) {
      const activities = JSON.parse(response);
      //JSPN parse response data
      //call place markers on map function - passing JSON response in
      addMarkersToMap(activities);
      console.log(activities);
    });
  };
}

//https://developer.mozilla.org/en-US/docs/Web/API/XMLHttpRequest/send#example_get
const loadJSON = (url, parseJSON) => {
  let xhr = new XMLHttpRequest();
  // 'open' the http request
  xhr.open("GET", url, true);
  // function handles what to do when the data is loaded / handles a failed request
  xhr.onload = function () {
    if (xhr.readyState === XMLHttpRequest.DONE && xhr.status === 200) {
      // Request finished. Do processing here  //response text = string
      const response = xhr.responseText;
      parseJSON(response);
    } else {
      console.log("request failed");
      //TODO: a more meaningful response on failed data
    }
  };
  //no data is being sent back becasue we want to fetch
  xhr.send(null);
};

function addMarkersToMap(activities) {
  //maybe it is better to use map here..
  activities.map((activity) => {
    const latLng = { lat: activity.location.lat, lng: activity.location.lng };
    const marker = new google.maps.Marker({
      position: latLng,
      map,
      icon: "http://127.0.0.1:5000/static/images/icons/run.svg",
      title: activity.description,
    });
    //add event listener to each marker
    marker.addListener("click", () => {
      displayActivity(activity);
    });
    return markers.push(marker);
  });
  //TODO add click functionality to marker - to display activity info when clicked
}

function clearMarkers() {
  if (markers) {
    markers.map((marker) => marker.setMap(null));
    console.log("markers cleared");
  } else {
    markers = [];
  }
}

function displayActivity(activity) {
  //when clicked i want to display information below
  document.getElementById("title").textContent = activity.title;
  document.getElementById("userName").textContent = activity.user_name;
  document.getElementById("activityType").textContent = activity.activity_type;
  document.getElementById("address").textConent = activity.address;
  document.getElementById("description").textContent = activity.description;

  console.log(activity);
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
