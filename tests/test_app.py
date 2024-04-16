import os
import pytest
from flask_testing import TestCase
from app import create_app
from services.temp_service import generate_temp_token


class MyTest(TestCase):
    def create_app(self):
        if not os.getenv('TEMP_SECRET_KEY'):
            os.environ['TEMP_SECRET_KEY'] = 'temp_secret_key'
        app = create_app()
        app.config['TESTING'] = True
        return app

    def test_home(self):
        response = self.client.get('/')
        self.assert200(response)
        self.assertEqual(response.data.decode(), 'Welcome to the Home Page!')

    def test_hello_world(self):
        response = self.client.get('/hello')
        self.assert200(response)
        self.assertEqual(response.json, {"message": "Hello World!"})

    def test_browser_automation(self):
        response = self.client.get('/test-browser')
        self.assert200(response)
        self.assertIn('pageTitle', response.json)
        self.assertIn('Browser automation successful', response.json['message'])

    def test_add_user(self):
        token = generate_temp_token('testuser')
        user_data = {
            "user_id": "testuser",
            "email": "testuser@example.com"
        }

        # First request to add a new user
        headers = {'Authorization': f'Bearer {token}'}
        response = self.client.post('/api/add-user', json=user_data, headers=headers)
        self.assertEqual(response.status_code, 201)

        # Second request with the same user data
        response = self.client.post('/api/add-user', json=user_data, headers=headers)
        self.assertNotEqual(response.status_code, 201, "Should not succeed")
        self.assertTrue('error' in response.json, "Should return error message")
        self.assertEqual(response.status_code, 409, "Should return a conflict status code (user already exists)")
