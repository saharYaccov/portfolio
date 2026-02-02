from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # הוספת תמיכה ב-CORS

latest_coords = {"lat": None, "lon": None}

@app.route("/location", methods=["POST"])
def location():
    data = request.json
    latest_coords["lat"] = data.get("lat")
    latest_coords["lon"] = data.get("lon")
    print(f"Received location: {latest_coords['lat']}, {latest_coords['lon']}")
    return jsonify({"status": "ok"})

@app.route("/location/latest", methods=["GET"])
def latest_location():
    if latest_coords["lat"] is None or latest_coords["lon"] is None:
        return jsonify({"error": "No location received yet"}), 404
    return jsonify(lat=latest_coords["lat"], lon=latest_coords["lon"])
@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "status": "ok",
        "message": "Bus Stop Alert API is running 🚍"
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
