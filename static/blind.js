let mediaRecorder;
let audioChunks = [];

async function startBlind() {
  // Start polling messages
  setInterval(fetchMessages, 3000);
}

async function sendGPS() {
  if(navigator.geolocation){
    navigator.geolocation.getCurrentPosition(async pos => {
      await fetch("/api/gps", {
        method:"POST",
        headers: {"Content-Type":"application/json"},
        body: JSON.stringify({lat: pos.coords.latitude, lng: pos.coords.longitude})
      });
      alert("Location sent to home user!");
    });
  }
}

async function sendVoiceMessage() {
  if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
    alert("Microphone not supported");
    return;
  }
  
  const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
  mediaRecorder = new MediaRecorder(stream);
  audioChunks = [];

  mediaRecorder.ondataavailable = e => {
    audioChunks.push(e.data);
  }

  mediaRecorder.onstop = async () => {
    const blob = new Blob(audioChunks, { type: 'audio/webm' });
    const arrayBuffer = await blob.arrayBuffer();
    const base64Audio = btoa(String.fromCharCode(...new Uint8Array(arrayBuffer)));

    await fetch("/api/send_message", {
      method:"POST",
      headers: {"Content-Type":"application/json"},
      body: JSON.stringify({sender:"blind", content: base64Audio, type:"voice"})
    });
    alert("Voice message sent!");
  }

  mediaRecorder.start();
  setTimeout(() => mediaRecorder.stop(), 5000); // record 5 seconds
}

async function fetchMessages() {
  let res = await fetch("/api/get_messages");
  let data = await res.json();
  let container = document.getElementById("messages");
  container.innerHTML = "";

  data.forEach(msg => {
    if(msg.sender === "home" && msg.type === "voice") {
      // Play TTS audio
      let audio = new Audio("data:audio/mp3;base64," + msg.content);
      audio.play();
      container.innerHTML += `<p>Home sent voice</p>`;
    } else if(msg.sender === "blind") {
      container.innerHTML += `<p>You sent a voice message</p>`;
    }
  });
}
