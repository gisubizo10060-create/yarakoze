const socket = io();
let map, marker, path;
let pathCoordinates = [];

function initMap() {
    map = new google.maps.Map(document.getElementById("map"), {
        center: { lat: 0, lng: 0 },
        zoom: 15
    });
    marker = new google.maps.Marker({
        position: { lat: 0, lng: 0 },
        map: map,
        title: "Blind Location"
    });
    path = new google.maps.Polyline({
        path: pathCoordinates,
        geodesic: true,
        strokeColor: "#FF0000",
        strokeOpacity: 1.0,
        strokeWeight: 3,
        map: map
    });
}

socket.on("location_update", loc => {
    const pos = { lat: loc.lat, lng: loc.lng };
    marker.setPosition(pos);
    map.setCenter(pos);
    pathCoordinates.push(pos);
    path.setPath(pathCoordinates);
});

socket.on("emergency_alert", data => {
    alert("Blind Emergency: " + data.message);
});

socket.on("voice_message", data => {
    alert(`${data.from} says: ${data.message}`);
});

// Send message from dashboard as voice (simulation)
document.getElementById("sendHomeMessage").addEventListener("click", () => {
    const msg = document.getElementById("homeMessage").value;
    if(msg) {
        fetch("/voice_from_home", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({message: msg})
        });
    }
});

// Initialize Google Map
window.onload = initMap;
