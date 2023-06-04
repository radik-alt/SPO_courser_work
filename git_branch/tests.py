from django.test import TestCase
from rest_framework.test import APIRequestFactory, APITestCase


# Create your tests here.
class TestApiLevels(APITestCase):
    def setUp(self):
        # Every test needs access to the request factory.
        self.factory = RequestFactory()

    def test_levels(self):
        # Create an instance of a GET request.
        request = self.factory.get('/customer/details')

        # Test my_view() as if it were deployed at /customer/details
        response = my_view(request)
        self.assertEqual(response.status_code, 200)
    def test_tasks(self):
        response = self.client.get("http://127.0.0.1:8000/api/v1/tasks")
        self.assertEqual(response.status_code, 200)


