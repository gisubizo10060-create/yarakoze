from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from flask_socketio import SocketIO, emit
import eventlet

eventlet.monkey_patch()  # Required for SocketIO with eventlet

app = Flask(__name__)
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")

# Store blind's current location
blind_location = {"lat": 0.0, "lng": 0.0}

@app.route('/')
def login_page():
    return render_template('login.html', error=None)

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/blind')
def blind_page():
    return render_template('blind.html')

@app.route('/update_location', methods=['POST'])
def update_location():
    global blind_location
    data = request.json
    blind_location['lat'] = data.get('lat', 0.0)
    blind_location['lng'] = data.get('lng', 0.0)
    socketio.emit('location_update', blind_location)
    return jsonify({"status": "ok"})

# Handle emergency button press
@app.route('/emergency', methods=['POST'])
def emergency():
    message = request.json.get('message', 'Emergency pressed!')
    socketio.emit('emergency_alert', {"message": message})
    return jsonify({"status": "alert_sent"})

# Voice message from blind
@app.route('/voice_from_blind', methods=['POST'])
def voice_from_blind():
    message = request.json.get('message', '')
    socketio.emit('voice_message', {"from": "blind", "message": message})
    return jsonify({"status": "sent"})

# Voice message from home user
@app.route('/voice_from_home', methods=['POST'])
def voice_from_home():
    message = request.json.get('message', '')
    socketio.emit('voice_message', {"from": "home", "message": message})
    return jsonify({"status": "sent"})

@socketio.on('connect')
def handle_connect():
    emit('location_update', blind_location)

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)
