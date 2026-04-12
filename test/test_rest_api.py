import unittest
import json
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "src"))

from rest_api import app


class RestApiTestCase(unittest.TestCase):

    def setUp(self):
        self.client = app.test_client()
        self.client.testing = True

    def test_invalid_temperature(self):
        payload = {
            "temperature": "bad",
            "timestamp": "2026-03-10T14:20:00Z"
        }

        response = self.client.post(
            "/temperature",
            data=json.dumps(payload),
            content_type="application/json"
        )

        self.assertEqual(response.status_code, 400)

    def test_missing_timestamp(self):
        payload = {
            "temperature": 24.5
        }

        response = self.client.post(
            "/temperature",
            data=json.dumps(payload),
            content_type="application/json"
        )

        self.assertEqual(response.status_code, 400)


if __name__ == "__main__":
    unittest.main()
