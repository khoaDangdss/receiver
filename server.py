# server.py (Updated with CORS)
from flask import Flask, request, jsonify
from flask_cors import CORS # <--- 1. NEW IMPORT

app = Flask(__name__)
CORS(app) # <--- 2. NEW LINE: Enables CORS for all routes

latest_data = {}

@app.route("/api/botdata", methods=["POST"])
def receive_data():
    global latest_data
    latest_data = request.json
    print("Received data:", latest_data)
    return jsonify({"status": "ok"}), 200


@app.route("/api/botdata", methods=["GET"])
def get_data():
    return jsonify(latest_data), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)