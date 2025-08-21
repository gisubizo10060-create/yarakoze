let map;
let marker;

// Initialize map
function initMap() {
    map = new google.maps.Map(document.getElementById("map"), {
        center: { lat: 0, lng: 0 },
        zoom: 15,
    });

    marker = new google.maps.Marker({
        position: { lat: 0, lng: 0 },
        map: map,
        title: "Blind Stick Location"
    });
}

// Update marker on the map
function updateMapMarker(lat, lng) {
    const position = { lat: lat, lng: lng };
    marker.setPosition(position);
    map.setCenter(position);
}

// Fetch updates every 3 seconds
setInterval(() => {
    fetch('/get_updates')
        .then(res => res.json())
        .then(data => {
            updateMapMarker(data.location.lat, data.location.lng);

            const messageContainer = document.getElementById('messages');
            messageContainer.innerHTML = '';
            data.messages.forEach(msg => {
                const p = document.createElement('p');
                p.textContent = msg;
                messageContainer.appendChild(p);
            });
        });
}, 3000);

// Initialize map after page load
window.onload = initMap;
