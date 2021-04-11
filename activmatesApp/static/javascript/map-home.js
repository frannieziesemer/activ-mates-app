// Note: This example requires that you consent to location sharing when
// prompted by your browser. If you see the error "The Geolocation service
// failed.", it means you probably did not give permission for the browser to
// locate you.
let map, infoWindow, markers, queryCenter, queryZoom;

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
  const locationButton = document.createElement("button");
  locationButton.textContent = "Pan to Current Location";
  locationButton.classList.add("pan-to-location-button");
  map.controls[google.maps.ControlPosition.TOP_CENTER].push(locationButton);

  const geocoder = new google.maps.Geocoder();

  document.getElementById("submit").addEventListener("click", () => {
    searchAddress(geocoder, map);
  });

  google.maps.event.addListener(map, "idle", function () {
    let newCenter = map.getCenter();
    let newZoom = map.getZoom();

    var distanceChange =
      queryCenter == null
        ? 0
        : google.maps.geometry.spherical.computeDistanceBetween(
            queryCenter,
            newCenter
          );

    if (
      queryCenter == null ||
      queryZoom == null ||
      distanceChange > 600 ||
      newZoom < queryZoom
    ) {
      //if we have not queried for markers yet, query
      renderData(newCenter, newZoom);
    }
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
  queryZoom = zoom;
  queryCenter = center;

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

const DEFAULT_ICON = {
  path:
    "M13.49,5.48 C14.59,5.48 15.49,4.58 15.49,3.48 C15.49,2.38 14.59,1.48 13.49,1.48 C12.39,1.48 11.49,2.38 11.49,3.48 C11.49,4.58 12.39,5.48 13.49,5.48 Z M10.32,17.48 L10.89,14.98 L12.99,16.98 L12.99,21.98 C12.99,22.53 13.44,22.98 13.99,22.98 C14.54,22.98 14.99,22.53 14.99,21.98 L14.99,16.34 C14.99,15.79 14.77,15.27 14.37,14.89 L12.89,13.48 L13.49,10.48 C14.56,11.72 16.11,12.61 17.85,12.89 C18.45,12.98 18.99,12.5 18.99,11.89 C18.99,11.4 18.63,10.99 18.14,10.91 C16.62,10.66 15.36,9.76 14.69,8.58 L13.69,6.98 C13.29,6.38 12.69,5.98 11.99,5.98 C11.69,5.98 11.49,6.08 11.19,6.08 L7.21,7.76 C6.47,8.08 5.99,8.8 5.99,9.61 L5.99,11.98 C5.99,12.53 6.44,12.98 6.99,12.98 C7.54,12.98 7.99,12.53 7.99,11.98 L7.99,9.58 L9.79,8.88 L8.19,16.98 L4.27,16.18 C3.73,16.07 3.2,16.42 3.09,16.96 L3.09,17 C2.98,17.54 3.33,18.07 3.87,18.18 L7.98,19 C9.04,19.21 10.08,18.54 10.32,17.48 Z",
  fillColor: "black",
  fillOpacity: 1,
  strokeColor: "black",
  strokeWeight: 0.7,
  scale: 1.3,
};

const SELECTED_ICON = {
  path:
    "M13.49,5.48 C14.59,5.48 15.49,4.58 15.49,3.48 C15.49,2.38 14.59,1.48 13.49,1.48 C12.39,1.48 11.49,2.38 11.49,3.48 C11.49,4.58 12.39,5.48 13.49,5.48 Z M10.32,17.48 L10.89,14.98 L12.99,16.98 L12.99,21.98 C12.99,22.53 13.44,22.98 13.99,22.98 C14.54,22.98 14.99,22.53 14.99,21.98 L14.99,16.34 C14.99,15.79 14.77,15.27 14.37,14.89 L12.89,13.48 L13.49,10.48 C14.56,11.72 16.11,12.61 17.85,12.89 C18.45,12.98 18.99,12.5 18.99,11.89 C18.99,11.4 18.63,10.99 18.14,10.91 C16.62,10.66 15.36,9.76 14.69,8.58 L13.69,6.98 C13.29,6.38 12.69,5.98 11.99,5.98 C11.69,5.98 11.49,6.08 11.19,6.08 L7.21,7.76 C6.47,8.08 5.99,8.8 5.99,9.61 L5.99,11.98 C5.99,12.53 6.44,12.98 6.99,12.98 C7.54,12.98 7.99,12.53 7.99,11.98 L7.99,9.58 L9.79,8.88 L8.19,16.98 L4.27,16.18 C3.73,16.07 3.2,16.42 3.09,16.96 L3.09,17 C2.98,17.54 3.33,18.07 3.87,18.18 L7.98,19 C9.04,19.21 10.08,18.54 10.32,17.48 Z",
  fillColor: "green",
  fillOpacity: 1,
  strokeColor: "green",
  strokeWeight: 0.7,
  scale: 1.3,
};

let selectedMarker = null;

function addMarkersToMap(activities) {
  activities.map((activity) => {
    const latLng = { lat: activity.location.lat, lng: activity.location.lng };
    const marker = new google.maps.Marker({
      position: latLng,
      title: activity.description,
      map: map,
      icon: DEFAULT_ICON,
    });

    // define info window content
    const contentString = `
      <div class="infoWindow">
        <h5>${activity.title}</h5>
        <a href=http://127.0.0.1:5000/activity/${activity.id} target="_blank"> more.. </a>
      </div>
    `;

    marker.profile = activity;

    //add event listener to each marker
    google.maps.event.addListener(marker, "click", () => {
      infoWindow = new google.maps.InfoWindow();
      infoWindow.setContent(contentString);
      infoWindow.open(map, marker);

      displayActivity(marker);
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
    selectedMarker = null;
  }
}

function displayActivity(marker) {
  if (selectedMarker) selectedMarker.setIcon(DEFAULT_ICON);

  marker.setIcon(SELECTED_ICON);
  //when clicked i want to display information below
  const card = document.querySelector(".activity-card");
  card.removeAttribute("hidden");
  document.getElementById("title").textContent = marker.profile.title;
  document.getElementById("userName").textContent = marker.profile.user_name;
  document.getElementById("activityType").textContent =
    marker.profile.activity_type;
  document.getElementById("address-display").textConent =
    marker.profile.address;
  document.getElementById("description").textContent =
    marker.profile.description;
  document.getElementById(
    "view-activity"
  ).href = `http://127.0.0.1:5000/activity/${marker.profile.id}`;
  document.getElementById(
    "activity-image"
  ).src = `static/images/activity-pics/${marker.profile.image}`;

  selectedMarker = marker;
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
