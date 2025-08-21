from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

# store blind's last location and message
blind_data = {"latitude": 0, "longitude": 0, "message": ""}

@app.route('/')
def home():
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/blind')
def blind():
    return render_template('blind.html')

@app.route('/update_location', methods=['POST'])
def update_location():
    global blind_data
    data = request.get_json()
    blind_data = data
    return jsonify({"status": "ok"})

@app.route('/get_location', methods=['GET'])
def get_location():
    return jsonify(blind_data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
