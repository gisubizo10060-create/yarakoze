# Blind Stick Tracker Dashboard

## Overview
This project is a **real-time tracking system** for visually impaired users (blind stick).  
It allows a home user to monitor the blind person's movement on a live map, receive obstacle alerts, and listen to voice messages sent by the blind person.

## Features
- **Home User Dashboard:**  
  - Login page (username: Yarakoze, password: rodger)  
  - Live map showing blind person's location  
  - Alerts for movement direction and obstacles  
  - Voice messages from blind person  

- **Blind Stick Mobile Interface:**  
  - Send movement directions (forward, left, right)  
  - Send obstacle alerts  
  - Send voice messages to home user  
  - Tracks GPS location via phone  

- **Backend Server:**  
  - Flask server handles data updates and provides latest information  
  - Endpoints:  
    - `POST /update` → receives data from blind stick  
    - `GET /latest` → sends latest data to dashboard  

- **Simulation Script:**  
  - `stick_test.py` can simulate blind stick data for testing  

## Technologies Used
- HTML, CSS, JavaScript (frontend)  
- Python Flask (backend)  
- Leaflet.js (interactive maps)  
- Flask-CORS (cross-origin requests)  

## Installation & Running Locally
1. Clone or download the project folder.  
2. Create a Python virtual environment:  
   ```bash
   python -m venv venv
