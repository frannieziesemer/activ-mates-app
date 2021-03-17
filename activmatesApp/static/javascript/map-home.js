// Note: This example requires that you consent to location sharing when
// prompted by your browser. If you see the error "The Geolocation service
// failed.", it means you probably did not give permission for the browser to
// locate you.
let map, infoWindow, markers;

function initMap() {
  //append map
  map = new google.maps.Map(document.getElementById("map"), {
    center: { lat: 52.52, lng: 13.405 },
    zoom: 10,
    streetViewControl: false,
    mapTypeControl: false,
    scaleControl: false,
    rotateControl: false,
    fullscreenControl: false,
  });
  //infoWindow = new google.maps.InfoWindow();
  const locationButton = document.createElement("button");
  locationButton.textContent = "Pan to Current Location";
  locationButton.classList.add("pan-to-location-button");
  map.controls[google.maps.ControlPosition.TOP_RIGHT].push(locationButton);

  const geocoder = new google.maps.Geocoder();

  document.getElementById("submit").addEventListener("click", () => {
    searchAddress(geocoder, map);
  });

  google.maps.event.addListener(map, "idle", function () {
    let center = map.getCenter();
    let zoom = map.getZoom();
    renderData(center, zoom);
  });
  // event listener for pan to current location
  locationButton.addEventListener("click", () => {
    // Try HTML5 geolocation.
    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(
        (position) => {
          const pos = {
            lat: position.coords.latitude,
            lng: position.coords.longitude,
          };
          // infoWindow.setPosition(pos);
          // infoWindow.setContent("Location found.");
          // infoWindow.open(map);
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
}
//convert zoom level provided by google to a value of meters
const zoomRadius = [
  800000, // zoom: 0
  800000, // zoom: 1
  800000, // zoom: 2
  800000, // zoom: 3
  800000, // zoom: 4
  800000, // zoom: 5
  800000, // zoom: 6
  400000, // zoom: 7
  200000, // zoom: 8
  100000, // zoom: 9
  51000, // zoom: 10
  26000, // zoom: 11
  13000, // zoom: 12
  6500, // zoom: 13
  3500, // zoom: 14
  1800, // zoom: 15
  900, // zoom: 16
  430, // zoom: 17
  210, // zoom: 18
  120, // zoom: 19
];

const renderData = (center, zoom) => {
  clearMarkers();
  const params = {
    lat: center.lat(),
    lng: center.lng(),
    radius: zoomRadius[zoom],
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

  loadJSON(newUrl);
};

const loadJSON = (url) => {
  fetch(url, { mode: "cors" })
    .then(function (response) {
      return response.json();
    })
    .then(function (response) {
      const activities = response;
      addMarkersToMap(activities);
    })
    .catch(function () {
      console.log("request failed");
    });
};

function addMarkersToMap(activities) {
  activities.map((activity) => {
    const latLng = { lat: activity.location.lat, lng: activity.location.lng };
    const marker = new google.maps.Marker({
      position: latLng,
      title: activity.description,
      map: map,
      //labelContent: '<span class="material-icons">directions_run</span>',
      labelAnchor: new google.maps.Point(22, 50),
    });
    //add event listener to each marker
    marker.addListener("click", () => {
      displayActivity(activity);
    });
    return markers.push(marker);
  });
  console.log(activities);
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
  const card = document.querySelector(".activity-card");
  card.toggleAttribute("hidden");
  document.getElementById("title").textContent = activity.title;
  document.getElementById("userName").textContent = activity.user_name;
  document.getElementById("activityType").textContent = activity.activity_type;
  document.getElementById("address").textConent = activity.address;
  document.getElementById("description").textContent = activity.description;
  document.getElementById(
    "view-activity"
  ).href = `http://127.0.0.1:5000/activity/${activity.id}`;
}

function searchAddress(geocoder, resultsMap) {
  const address = document.getElementById("address").value;
  geocoder.geocode({ address: address }, (results, status) => {
    if (status === "OK") {
      resultsMap.setCenter(results[0].geometry.location);
      resultsMap.setZoom(12);
    } else {
      alert("Geocode was not successful for the following reason: " + status);
    }
  });
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
