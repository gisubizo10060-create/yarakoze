// Emergency button
document.getElementById('emergency').addEventListener('click', () => {
    fetch('/send_message', {
        method:'POST',
        headers:{'Content-Type':'application/json'},
        body:JSON.stringify({message:'Emergency!'})
    });
});

// Voice recording
let mediaRecorder;
let audioChunks = [];

document.getElementById('recordBtn').addEventListener('click', async () => {
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
    mediaRecorder = new MediaRecorder(stream);
    audioChunks = [];

    mediaRecorder.ondataavailable = e => audioChunks.push(e.data);
    mediaRecorder.onstop = async () => {
        const blob = new Blob(audioChunks, {type:'audio/wav'});
        const formData = new FormData();
        formData.append('audio', blob, 'voice.wav');
        await fetch('/upload_audio', {method:'POST', body: formData});
    };

    mediaRecorder.start();
    document.getElementById('stopBtn').disabled = false;
});

document.getElementById('stopBtn').addEventListener('click', () => {
    mediaRecorder.stop();
    document.getElementById('stopBtn').disabled = true;
});

// Simulate sending GPS location
setInterval(() => {
    navigator.geolocation.getCurrentPosition(async (pos) => {
        await fetch('/update_location', {
            method:'POST',
            headers:{'Content-Type':'application/json'},
            body: JSON.stringify({lat: pos.coords.latitude, lng: pos.coords.longitude})
        });
    });
}, 3000);
