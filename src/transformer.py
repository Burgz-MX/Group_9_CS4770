from flask import Flask, request, jsonify

app = Flask(__name__)


def voltage_to_temperature(voltage):
    """
    Simple conversion formula for class demo:
    temperature (C) = voltage * 10
    Example: 2.75V -> 27.5C
    """
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

    return jsonify({
        "sensorId": sensor_id,
        "temperature": temperature,
        "unit": "C",
        "timestamp": timestamp,
        "status": "success"
    }), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)
