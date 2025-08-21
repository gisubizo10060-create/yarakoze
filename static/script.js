async function updateDashboard(){
    try{
        const serverUrl = window.location.origin; // automatically uses Render URL
        const res = await fetch(`${serverUrl}/latest`);
        const data = await res.json();

        const statusDiv = document.getElementById("stickStatus");
        if(statusDiv){
            statusDiv.innerText = `Direction: ${data.direction || 'N/A'}, Obstacle: ${data.obstacle || false}`;
        }

        const voiceDiv = document.getElementById("voiceMessages");
        if(data.voice && data.voice !== ""){
            voiceDiv.innerText = `Voice: ${data.voice}`;
        }

        if(data.latitude && data.longitude){
            if(!window.map){
                window.map = L.map('map').setView([data.latitude, data.longitude], 16);
                L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
                    maxZoom: 19
                }).addTo(window.map);
                window.marker = L.marker([data.latitude, data.longitude]).addTo(window.map);
            } else {
                window.marker.setLatLng([data.latitude, data.longitude]);
                window.map.setView([data.latitude, data.longitude]);
            }
        }

    } catch(e){
        console.error(e);
    }
}

setInterval(updateDashboard, 2000);
