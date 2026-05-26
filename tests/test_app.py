# test_app.py
import unittest
from src.app import app
from src.config.settings import (
    APP_VERSION,
    APP_ENVIRONMENT
)


class HealthApiTest(unittest.TestCase):

    def setUp(self):
        self.client = app.test_client()
        self.client.testing = True

    # Happy Path Test
    def test_health_endpoint_success(self):
        response = self.client.get("/health")

        self.assertEqual(response.status_code, 200)

        data = response.get_json()

        self.assertEqual(data["status"], "healthy")
        self.assertEqual(data["version"], APP_VERSION)
        self.assertEqual(data["environment"], APP_ENVIRONMENT)

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