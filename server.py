from flask import Flask, render_template, request, jsonify, redirect, url_for
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Mock user data
users = {"yarakoze": "rodger"}

# Store blind locations and messages
blind_data = {"location": None, "messages": []}

@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if users.get(username) == password:
            return redirect(url_for('dashboard'))
        else:
            error = "Invalid username or password!"
    return render_template('login.html', error=error)

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html', blind_data=blind_data)

@app.route('/blind')
def blind():
    return render_template('blind.html')

@app.route('/send_location', methods=['POST'])
def send_location():
    data = request.json
    blind_data['location'] = data
    return jsonify({'message': 'Location sent!'})

@app.route('/send_message', methods=['POST'])
def send_message():
    data = request.json
    blind_data['messages'].append(data['message'])
    return jsonify({'message': 'Message sent!'})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
