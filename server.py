from flask import Flask, request, jsonify, render_template, redirect, url_for, session
from flask_cors import CORS

app = Flask(__name__)
app.secret_key = "your_secret_key"  # Required for session
CORS(app)

latest_data = {}

# Fake user credentials
USER_CREDENTIALS = {"Yarakoze": "rodger"}

# API endpoint for blind stick
@app.route('/update', methods=['POST'])
def update_data():
    global latest_data
    latest_data = request.json
    return jsonify({"status": "success"}), 200

@app.route('/latest', methods=['GET'])
def get_latest():
    return jsonify(latest_data), 200

# Login page
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username in USER_CREDENTIALS and USER_CREDENTIALS[username] == password:
            session['user'] = username
            return redirect(url_for('dashboard'))
        else:
            return render_template('login.html', error="Invalid credentials")
    return render_template('login.html', error=None)

# Dashboard page
@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template('dashboard.html')

# Blind stick page
@app.route('/blind')
def blind():
    return render_template('blind.html')

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
