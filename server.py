from flask import Flask, render_template, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Global variables
latest_location = {}
gps_path = []
voice_messages = []

# --- HOME USER ---
@app.route('/')
def login():
    return render_template('login.html', error=None)

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

# --- BLIND ---
@app.route('/blind')
def blind():
    return render_template('blind.html')

# --- API ENDPOINTS ---
@app.route("/api/gps", methods=["POST"])
def gps():
    global latest_location, gps_path
    data = request.json
    latest_location = {"lat": data["lat"], "lng": data["lng"]}
    gps_path.append(latest_location)
    return jsonify({"status": "ok"})

@app.route("/api/get_gps")
def get_gps():
    return jsonify(latest_location)

@app.route("/api/get_path")
def get_path():
    return jsonify({"path": gps_path})

@app.route("/api/send_message", methods=["POST"])
def send_message():
    data = request.json
    voice_messages.append(data)  # {sender, content}
    return jsonify({"status": "ok"})

@app.route("/api/get_messages")
def get_messages():
    return jsonify(voice_messages)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
