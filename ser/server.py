from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Store blind location and messages
blind_data = {
    'location': {'lat': 0, 'lng': 0},
    'messages': []
}

@app.route('/')
def dashboard():
    return render_template('dashboard.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username == 'yarakoze' and password == 'rodger':
            return render_template('dashboard.html')
        else:
            error = 'Invalid credentials'
    return render_template('login.html', error=error)

@app.route('/blind', methods=['POST'])
def blind_update():
    data = request.json
    if 'lat' in data and 'lng' in data:
        blind_data['location']['lat'] = data['lat']
        blind_data['location']['lng'] = data['lng']
    if 'message' in data:
        blind_data['messages'].append(data['message'])
    return jsonify({'status': 'success'})

@app.route('/get_location')
def get_location():
    return jsonify(blind_data['location'])

@app.route('/get_messages')
def get_messages():
    return jsonify(blind_data['messages'])

if __name__ == "__main__":
    app.run(debug=True)
