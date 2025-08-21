from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

# Store latest data
latest_data = {
    "latitude": 0,
    "longitude": 0,
    "direction": "",
    "obstacle": False,
    "voice": ""
}

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/blind')
def blind():
    return render_template('blind.html')

@app.route('/update', methods=['POST'])
def update_location():
    global latest_data
    data = request.get_json()
    latest_data.update(data)
    return jsonify({"status": "ok"})

@app.route('/location', methods=['GET'])
def get_location():
    return jsonify(latest_data)

if __name__ == "__main__":
    app.run(debug=True)
