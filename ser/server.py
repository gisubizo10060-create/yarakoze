from flask import Flask, render_template, request, redirect, session, jsonify, send_file
from flask_cors import CORS
from flask_socketio import SocketIO
from gtts import gTTS
import os, time

app = Flask(__name__)
app.secret_key = "supersecret"
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")

# ----- In-memory state -----
BLIND_STATE = {
    "location": None,
    "messages": [],
    "emergency": False,
    "voice_files": []
}

# ----- Login -----
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if username == "homeuser" and password == "1234":
            session["user"] = username
            return redirect("/dashboard")
        else:
            return render_template("login.html", error="Invalid login")
    return render_template("login.html", error=None)

# ----- Dashboard -----
@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect("/")
    return render_template("dashboard.html")

# ----- Blind interface -----
@app.route("/blind")
def blind():
    return render_template("blind.html")

# ----- APIs -----
@app.route("/api/gps", methods=["POST"])
def update_gps():
    BLIND_STATE["location"] = request.json
    socketio.emit("gps_update", BLIND_STATE["location"])
    return jsonify({"status": "ok"})

@app.route("/api/emergency", methods=["POST"])
def emergency():
    BLIND_STATE["emergency"] = True
    socketio.emit("emergency_alert", {"time": time.time()})
    return jsonify({"status": "alert sent"})

@app.route("/api/send_voice", methods=["POST"])
def send_voice():
    file = request.files["voice"]
    path = f"static/voice_{int(time.time())}.wav"
    file.save(path)
    BLIND_STATE["voice_files"].append(path)
    socketio.emit("voice_message", {"file": path})
    return jsonify({"status": "voice sent"})

@app.route("/api/send_message", methods=["POST"])
def send_message():
    msg = request.json["text"]
    # Convert text to speech
    tts = gTTS(msg)
    filename = f"static/tts_{int(time.time())}.mp3"
    tts.save(filename)
    BLIND_STATE["messages"].append(filename)
    socketio.emit("new_message", {"text": msg})
    return jsonify({"status": "message sent"})

@app.route("/api/get_messages", methods=["GET"])
def get_messages():
    if BLIND_STATE["messages"]:
        file = BLIND_STATE["messages"].pop(0)
        return send_file(file, as_attachment=True)
    return jsonify({"status": "no messages"})

if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=5000)
