# test_app.py
import unittest
from src.app import app


class HealthApiTest(unittest.TestCase):

    def setUp(self):
        self.client = app.test_client()
        self.client.testing = True

    # Happy Path Test
    def test_health_endpoint_success(self):
        response = self.client.get("/health")

        self.assertEqual(response.status_code, 200)

        data = response.get_json()

        self.assertEqual(data["status"], "running")
        self.assertEqual(data["version"], "1.0.0")
        self.assertEqual(data["environment"], "dev")

        self.assertIn("timestamp", data)

    # Edge Case - POST not allowed
    def test_health_endpoint_post_not_allowed(self):
        response = self.client.post("/health")

        self.assertEqual(response.status_code, 405)


    # Edge Case - PUT not allowed
    def test_health_endpoint_put_not_allowed(self):
        response = self.client.put("/health")

        self.assertEqual(response.status_code, 405)

    # Edge Case Test
    def test_invalid_endpoint(self):
        response = self.client.get("/invalid-endpoint")

        self.assertEqual(response.status_code, 404)


if __name__ == "__main__":
    unittest.main()