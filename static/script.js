const map = L.map('map').setView([0, 0], 2);

L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; OpenStreetMap contributors'
}).addTo(map);

let stickMarker = null;
let pathCoordinates = [];
let pathLine = null;

function updateBlindLocation(data) {
    const { latitude, longitude, direction, obstacle, voice } = data;
    const latlng = [latitude, longitude];

    if (!stickMarker) {
        stickMarker = L.marker(latlng).addTo(map);
        map.setView(latlng, 16);
    } else {
        stickMarker.setLatLng(latlng);
    }

    pathCoordinates.push(latlng);
    if (pathLine) {
        pathLine.setLatLngs(pathCoordinates);
    } else {
        pathLine = L.polyline(pathCoordinates, { color: 'red', weight: 4 }).addTo(map);
    }

    document.getElementById('stickStatus').innerText = `Direction: ${direction || 'N/A'}, Obstacle: ${obstacle ? 'Yes' : 'No'}`;
    if (voice) document.getElementById('voiceMessages').innerText = voice;
}

setInterval(async () => {
    try {
        const res = await fetch('/location');
        const data = await res.json();
        updateBlindLocation(data);
    } catch (err) {
        console.error('Error fetching location:', err);
    }
}, 2000);
