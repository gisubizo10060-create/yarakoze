document.getElementById('send-location').addEventListener('click', () => {
    navigator.geolocation.getCurrentPosition(position => {
        const data = {
            lat: position.coords.latitude,
            lng: position.coords.longitude
        };

        fetch('/send_location', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        })
        .then(res => res.json())
        .then(response => {
            document.getElementById('status').textContent = response.message;
        });
    }, err => {
        document.getElementById('status').textContent = "Location access denied!";
    });
});

document.getElementById('send-message').addEventListener('click', () => {
    const msg = prompt("Type your message:");
    if (msg) {
        fetch('/send_message', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ message: msg })
        })
        .then(res => res.json())
        .then(response => {
            document.getElementById('status').textContent = response.message;
        });
    }
});
