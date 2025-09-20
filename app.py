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

if __name__ == '__main__':
    app.run(debug=True)
