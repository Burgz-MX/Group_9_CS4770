from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

REST_API_URL = "http://localhost:6000/temperature"


def voltage_to_temperature(voltage):
    return round(voltage * 10, 2)


@app.route("/transform", methods=["POST"])
def transform():
    data = request.get_json()

    if not data:
        return jsonify({
            "status": "error",
            "message": "Request body must be valid JSON"
        }), 400

    sensor_id = data.get("sensorId")
    sampled_voltage = data.get("sampledVoltage")
    timestamp = data.get("timestamp")

    if not sensor_id or not isinstance(sensor_id, str):
        return jsonify({
            "status": "error",
            "message": "sensorId must be a string"
        }), 400

    if not isinstance(sampled_voltage, (int, float)):
        return jsonify({
            "status": "error",
            "message": "sampledVoltage must be a number"
        }), 400

    if not timestamp or not isinstance(timestamp, str):
        return jsonify({
            "status": "error",
            "message": "timestamp must be a string"
        }), 400

    temperature = voltage_to_temperature(sampled_voltage)

    try:
        rest_response = requests.post(REST_API_URL, json={
            "temperature": temperature,
            "timestamp": timestamp
        })
        rest_data = rest_response.json()
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": "REST API unavailable",
            "details": str(e)
        }), 500

    return jsonify({
        "sensorId": sensor_id,
        "temperature": temperature,
        "unit": "C",
        "timestamp": timestamp,
        "storage": rest_data,
        "status": "success"
    }), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
