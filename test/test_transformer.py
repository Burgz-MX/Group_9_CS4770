import unittest
import json
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "src"))

from transformer import app, voltage_to_temperature


class TransformerTestCase(unittest.TestCase):

    def setUp(self):
        self.client = app.test_client()
        self.client.testing = True

    def test_voltage_to_temperature_conversion(self):
        self.assertEqual(voltage_to_temperature(2.5), 25.0)
        self.assertEqual(voltage_to_temperature(0), 0)
        self.assertEqual(voltage_to_temperature(3.33), 33.3)

    def test_valid_transform_request(self):
        payload = {
            "sensorId": "sensor-1",
            "sampledVoltage": 2.75,
            "timestamp": "2026-03-20T16:00:00Z"
        }

        response = self.client.post(
            "/transform",
            data=json.dumps(payload),
            content_type="application/json"
        )

        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data["status"], "success")
        self.assertEqual(data["temperature"], 27.5)

    def test_invalid_voltage(self):
        payload = {
            "sensorId": "sensor-1",
            "sampledVoltage": "bad",
            "timestamp": "2026-03-20T16:00:00Z"
        }

        response = self.client.post(
            "/transform",
            data=json.dumps(payload),
            content_type="application/json"
        )

        self.assertEqual(response.status_code, 400)
        data = response.get_json()
        self.assertEqual(data["status"], "error")

    def test_missing_json(self):
        response = self.client.post("/transform")
        self.assertEqual(response.status_code, 400)


if __name__ == "__main__":
    unittest.main()
