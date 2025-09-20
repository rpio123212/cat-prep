from flask import Flask, request, jsonify
from flask_cors import CORS
import pyrebase
import time

app = Flask(__name__)
CORS(app)

# Firebase config (directly from your provided creds)
firebaseConfig = {
    "apiKey": "AIzaSyBlnWSLpgV1qGPNRfk69i6__9YsEDLb8O4",
    "authDomain": "cat-data-4daff.firebaseapp.com",
    "databaseURL": "https://cat-data-4daff-default-rtdb.firebaseio.com",
    "projectId": "cat-data-4daff",
    "storageBucket": "cat-data-4daff.firebasestorage.app",
    "messagingSenderId": "823064000399",
    "appId": "1:823064000399:web:15bd7387f362d2f254bdfa",
    "measurementId": "G-4437FGB845"
}

# Initialize Firebase
firebase = pyrebase.initialize_app(firebaseConfig)
db = firebase.database()

from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes, all domains

@app.route('/')
def hello_world():
    return 'Hello, World!'

# New GET endpoint
@app.route('/get', methods=['GET'])
def get_data():
    return jsonify({
        "message": "This is a GET response",
        "status": "success"
    })


# POST 1: Store test results
@app.route('/add_test', methods=['POST'])
def add_test():
    data = request.json
    if not data:
        return jsonify({"error": "Missing JSON body"}), 400

    entry = {
        "score": data.get("score"),
        "percentile": data.get("percentile"),
        "remarks": data.get("remarks"),
        "improvements": data.get("improvements"),
        "others": data.get("others"),
        "rating": data.get("rating", 0),
        "timestamp": int(time.time())
    }
    db.child("test-output").push(entry)
    return jsonify({"message": "Test data added successfully", "data": entry}), 201


# POST 2: Store daily progress
@app.route('/add_day', methods=['POST'])
def add_day():
    data = request.json
    if not data:
        return jsonify({"error": "Missing JSON body"}), 400

    entry = {
        "activities": data.get("activities"),
        "rating": data.get("rating", 0),
        "timestamp": int(time.time())
    }
    db.child("daily-progress").push(entry)
    return jsonify({"message": "Daily progress added successfully", "data": entry}), 201


# GET 3: Retrieve data
@app.route('/get_data', methods=['GET'])
def get_data():
    data_type = request.args.get("type")
    if not data_type:
        return jsonify({"error": "Missing query param ?type=exams or ?type=days"}), 400

    if data_type == "exams":
        data = db.child("test-output").get().val() or {}
        return jsonify({"exams": data})

    elif data_type == "days":
        data = db.child("daily-progress").get().val() or {}
        return jsonify({"days": data})

    else:
        return jsonify({"error": "Invalid type. Use 'exams' or 'days'"}), 400


if __name__ == '__main__':
    app.run(debug=True)
