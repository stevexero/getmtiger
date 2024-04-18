import os
import pytest
from flask_testing import TestCase
from unittest.mock import patch
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

    # @patch('services.temp_service.decode_clerk_token')
    @patch('routes.user_routes.decode_clerk_token')
    @patch('services.user_service.add_user_to_database')
    # def test_add_user(self):
    def test_add_user(self, mock_add_user_to_database, mock_decode_clerk_token):
        # Setup mocks
        mock_decode_clerk_token.return_value = ('testuser', None)
        # mock_add_user_to_database.return_value = ({"user_id": "testuser", "email": "testuser@example.com"}, None, 201)
        mock_add_user_to_database.side_effect = [
            ({"user_id": "testuser", "email": "testuser@example.com"}, None, 201),  # First call success
            (None, 'User with this ID or Email already exists', 409)  # Second call fail
        ]

        token = generate_temp_token('testuser')
        user_data = {
            "user_id": "testuser",
            "email": "testuser@example.com"
        }

        # First request to add a new user
        headers = {'Authorization': f'Bearer {token}'}
        response = self.client.post('/api/add-user', json=user_data, headers=headers)

        # Verify that the add user function was called with the correct data
        # mock_add_user_to_database.assert_called_once_with(user_data)

        self.assertEqual(response.status_code, 201)

        # Second request with the same user data
        # response = self.client.post('/api/add-user', json=user_data, headers=headers)
        # self.assertNotEqual(response.status_code, 201, "Should not succeed")
        # self.assertTrue('error' in response.json, "Should return error message")
        # self.assertEqual(response.status_code, 409, "Should return a conflict status code (user already exists)")

        # mock_add_user_to_database.return_value = (None, 'User with this ID or Email already exists', 409)
        response = self.client.post('/api/add-user', json=user_data, headers=headers)
        # self.assertNotEqual(response.status_code, 201)
        self.assertIn('error', response.json)
        self.assertEqual(response.json['error'], 'User with this ID or Email already exists')
        # self.assertEqual(response.status_code, 409)
