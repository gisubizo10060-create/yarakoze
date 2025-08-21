const socket = io();

const emergencyBtn = document.getElementById("emergency-btn");
const voiceBtn = document.getElementById("voice-btn");

// Send emergency alert
emergencyBtn.addEventListener("click", () => {
    fetch("/emergency", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({message: "Emergency pressed!"})
    });
});

// Send voice message (placeholder, you can integrate real voice capture)
voiceBtn.addEventListener("click", () => {
    const msg = prompt("Record message for home user:");
    if(msg) {
        fetch("/voice_from_blind", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({message: msg})
        });
    }
});

// Send location periodically
function sendLocation() {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(pos => {
            fetch("/update_location", {
                method: "POST",
                headers: {"Content-Type": "application/json"},
                body: JSON.stringify({
                    lat: pos.coords.latitude,
                    lng: pos.coords.longitude
                })
            });
        });
    }
}
setInterval(sendLocation, 5000);
