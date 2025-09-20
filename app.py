from flask import Flask, request, jsonify
from flask_cors import CORS
import firebase_admin
from firebase_admin import credentials, db
import time

app = Flask(__name__)
CORS(app)

# --- Firebase Admin Config (works with latest Python) ---
# Instead of pyrebase, we use firebase_admin with service account
# Get the service account JSON from Firebase Console -> Project Settings -> Service Accounts
cred = credentials.Certificate("creds.json")  # place JSON file in project root
firebase_admin.initialize_app(cred, {
    'databaseURL': "https://cat-data-4daff-default-rtdb.firebaseio.com/"
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
    ref = db.reference('test-output')
    ref.push(entry)
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
    ref = db.reference('daily-progress')
    ref.push(entry)
    return jsonify({"message": "Daily progress added successfully", "data": entry}), 201


# GET 3: Retrieve data
@app.route('/get_data', methods=['GET'])
def get_data():
    data_type = request.args.get("type")
    if not data_type:
        return jsonify({"error": "Missing query param ?type=exams or ?type=days"}), 400

    if data_type == "exams":
        ref = db.reference('test-output')
        data = ref.get() or {}
        return jsonify({"exams": data})

    elif data_type == "days":
        ref = db.reference('daily-progress')
        data = ref.get() or {}
        return jsonify({"days": data})

    else:
        return jsonify({"error": "Invalid type. Use 'exams' or 'days'"}), 400


if __name__ == '__main__':
    app.run(debug=True)
