from flask import Flask, render_template
from flask_socketio import SocketIO, emit

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

# Store blind's path
blind_path = []

@app.route('/')
def dashboard():
    return render_template('dashboard.html')

@app.route('/blind')
def blind():
    return render_template('blind.html')

# Receive location from blind
@socketio.on('location_update')
def handle_location(data):
    blind_path.append((data['lat'], data['lng']))
    emit('update_map', {'location': data, 'path': blind_path}, broadcast=True)

# Emergency alert from blind
@socketio.on('emergency')
def handle_emergency(data):
    emit('emergency_alert', data, broadcast=True)

# Send message from home to blind
@socketio.on('message_to_blind')
def message_to_blind(data):
    emit('text_for_blind', data, broadcast=True)

# Send voice message from blind to home
@socketio.on('voice_to_home')
def voice_to_home(data):
    emit('voice_from_blind', data, broadcast=True)

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)
