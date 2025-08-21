import requests
import time
import random

# Use your Render server URL
url = "https://blind-stick-dashboard.onrender.com/update"

while True:
    # Simulate GPS, direction, obstacle, and voice
    data = {
        "latitude": 1.95 + random.random()*0.01,
        "longitude": 30.06 + random.random()*0.01,
        "direction": random.choice(["forward","left","right"]),
        "obstacle": random.choice([True, False]),
        "voice": random.choice(["","Hello","Help me!"])
    }
    
    # Send data to Render server
    try:
        response = requests.post(url, json=data)
        print("Sent:", data, "| Status:", response.status_code)
    except Exception as e:
        print("Error:", e)

    # Wait 2 seconds before sending next update
    time.sleep(2)
