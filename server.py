from flask import Flask, request, jsonify

app = Flask(__name__)

# store data here (memory storage)
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
