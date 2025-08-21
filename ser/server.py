from flask import Flask, render_template, request, jsonify, send_from_directory
from flask_cors import CORS
import os
import time

app = Flask(__name__)
CORS(app)

# Create folder for audio files
os.makedirs('audio', exist_ok=True)

blind_location = {'lat': 1.944, 'lng': 30.061}
messages = []

@app.route('/')
def login():
    return render_template('login.html', error=None)

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/blind')
def blind():
    return render_template('blind.html')

@app.route('/update_location', methods=['POST'])
def update_location():
    data = request.json
    blind_location['lat'] = data.get('lat', blind_location['lat'])
    blind_location['lng'] = data.get('lng', blind_location['lng'])
    return jsonify(status='ok')

@app.route('/get_location')
def get_location():
    return jsonify(blind_location)

# Text messages
@app.route('/send_message', methods=['POST'])
def send_message():
    msg = request.json.get('message')
    if msg:
        messages.append(f"Blind: {msg}")
    return jsonify(status='ok')

@app.route('/send_home_message', methods=['POST'])
def send_home_message():
    msg = request.json.get('message')
    if msg:
        messages.append(f"Home: {msg}")
    return jsonify(status='ok')

@app.route('/get_messages')
def get_messages():
    return jsonify(messages)

# Upload audio from blind or home
@app.route('/upload_audio', methods=['POST'])
def upload_audio():
    audio_file = request.files['audio']
    filename = f"audio/{int(time.time())}.wav"
    audio_file.save(filename)
    messages.append(f"Audio message: {filename}")
    return jsonify(status='ok')

# Serve audio files
@app.route('/audio/<filename>')
def get_audio(filename):
    return send_from_directory('audio', filename)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
