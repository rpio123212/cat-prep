from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import time

app = Flask(__name__)
CORS(app)

# Firebase Realtime Database base URL
BASE_URL = "https://cat-data-4daff-default-rtdb.firebaseio.com"

def push_to_firebase(path, data):
    url = f"{BASE_URL}/{path}.json"
    res = requests.post(url, json=data)
    if res.status_code == 200:
        return res.json()
    else:
        return {"error": res.text}

def get_from_firebase(path):
    url = f"{BASE_URL}/{path}.json"
    res = requests.get(url)
    if res.status_code == 200:
        return res.json()
    else:
        return {"error": res.text}

@app.route("/add_test", methods=["POST"])
def add_test():
    data = request.get_json()
    entry = {
        "score": data.get("score"),
        "percentile": data.get("percentile"),
        "remarks": data.get("remarks"),
        "improvements": data.get("improvements"),
        "others": data.get("others"),
        "rating": data.get("rating"),
        "timestamp": int(time.time())
    }
    result = push_to_firebase("test-output", entry)
    return jsonify({"message": "Test data added", "firebase_result": result, "data": entry})

@app.route("/add_day", methods=["POST"])
def add_day():
    data = request.get_json()
    entry = {
        "summary": data.get("summary"),
        "rating": data.get("rating"),
        "timestamp": int(time.time())
    }
    result = push_to_firebase("daily-output", entry)
    return jsonify({"message": "Day data added", "firebase_result": result, "data": entry})

@app.route("/get_data", methods=["GET"])
def get_data():
    query = request.args.get("type")
    if query == "tests":
        data = get_from_firebase("test-output")
    elif query == "days":
        data = get_from_firebase("daily-output")
    else:
        return jsonify({"error": "Invalid query param. Use ?type=tests or ?type=days"}), 400
    return jsonify(data)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
