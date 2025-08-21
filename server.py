from flask import Flask, render_template, request
from flask_cors import CORS
from flask_socketio import SocketIO, emit

app = Flask(__name__)
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")

blind_location = {"lat": 0, "lng": 0}

@app.route('/')
def home():
    return render_template('dashboard.html')

@app.route('/blind')
def blind():
    return render_template('blind.html')

@app.route('/update_location', methods=['POST'])
def update_location():
    global blind_location
    data = request.json
    blind_location = {"lat": data["lat"], "lng": data["lng"]}
    socketio.emit('location_update', blind_location)
    return {"status": "ok"}

@app.route('/emergency', methods=['POST'])
def emergency():
    data = request.json
    socketio.emit('emergency_alert', {"message": data["message"]})
    return {"status": "alert sent"}

@app.route('/voice_from_blind', methods=['POST'])
def voice_from_blind():
    data = request.json
    socketio.emit('voice_message', {"from": "blind", "message": data["message"]})
    return {"status": "voice sent"}

@app.route('/voice_from_home', methods=['POST'])
def voice_from_home():
    data = request.json
    socketio.emit('voice_message', {"from": "home", "message": data["message"]})
    return {"status": "voice sent"}

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000)
