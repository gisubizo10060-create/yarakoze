let map, marker, pathLine;

function initMap() {
  map = new google.maps.Map(document.getElementById("map"), {
    zoom: 15,
    center: { lat: -1.95, lng: 30.1 }
  });
  marker = new google.maps.Marker({ map });
  pathLine = new google.maps.Polyline({
    path: [],
    geodesic: true,
    strokeColor: "#FF0000",
    strokeOpacity: 1.0,
    strokeWeight: 4,
    map: map
  });
}

async function fetchGPS() {
  let res = await fetch("/api/get_gps");
  let data = await res.json();
  if (data.lat) {
    let pos = {lat: data.lat, lng: data.lng};
    marker.setPosition(pos);
    map.setCenter(pos);
  }
  fetchPath();
}

async function fetchPath() {
  let res = await fetch("/api/get_path");
  let data = await res.json();
  let pathCoords = data.path.map(p => ({lat: p.lat, lng: p.lng}));
  pathLine.setPath(pathCoords);
}

async function sendMessage() {
  let content = document.getElementById("messageInput").value;
  if(!content) return;
  await fetch("/api/send_message", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({sender:"home", content})
  });
  document.getElementById("messageInput").value = "";
}

function startTracking() {
  fetchGPS();
  setInterval(fetchGPS, 5000);
}
