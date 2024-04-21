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

    @patch('routes.user_routes.decode_clerk_token')
    @patch('services.user_service.add_user_to_database')
    @patch('services.user_service.get_user_from_database')
    def test_user_management(self, mock_get_user_from_database, mock_add_user_to_database, mock_decode_clerk_token):
        # Set up the mock responses
        user_id = 'user_id_of_testuser'
        email = 'testuser@example.com'
        user_data = {"user_id": user_id, "email": email}
        mock_decode_clerk_token.return_value = (user_id, None)
        mock_add_user_to_database.return_value = (user_data, None, 201)
        mock_get_user_from_database.return_value = ([user_data], None, 200)

        token = generate_temp_token(user_id)
        headers = {'Authorization': f'Bearer {token}'}

        # 1. Add a user
        response = self.client.post('/api/add-user', json=user_data, headers=headers)
        self.assertEqual(response.status_code, 201)

        # 2. Try adding the same user again (expect failure due to duplicate)
        mock_add_user_to_database.return_value = (None, 'User with this ID or Email already exists', 409)
        response_duplicate = self.client.post('/api/add-user', json=user_data, headers=headers)
        self.assertEqual(response_duplicate.status_code, 409)

        # 3. Retrieve the current user
        response_current_user = self.client.get('/api/get-current-user', headers=headers)
        self.assertEqual(response_current_user.status_code, 200)

        # Verifying mock calls
        mock_decode_clerk_token.assert_called_with(token)
        mock_add_user_to_database.assert_called()
        mock_get_user_from_database.assert_called_with(user_id)

    # Decorators used to replace the actual functions with mock objects and simulate their responses
    # @patch('routes.user_routes.decode_clerk_token')
    # @patch('services.user_service.add_user_to_database')
    # # Defines the test method and mock objects (created by the @patch decorators) as arguments that allow you to define
    # # their return values
    # def test_add_user(self, mock_add_user_to_database, mock_decode_clerk_token):
    #     # Configure the mock to always return 'x' value(s)
    #     mock_decode_clerk_token.return_value = ('user_id_of_testuser', None)
    #     mock_add_user_to_database.return_value = ({"user_id": "user_id_of_testuser", "email": "testuser@example.com"}, None, 201)
    #
    #     token = generate_temp_token('user_id_of_testuser')
    #     user_data = {
    #         "user_id": "user_id_of_testuser",
    #         "email": "testuser@example.com"
    #     }
    #     headers = {'Authorization': f'Bearer {token}'}
    #
    #     response = self.client.post('/api/add-user', json=user_data, headers=headers)
    #
    #     self.assertEqual(response.status_code, 201)
    #     self.assertEqual(response.json['user_id'], 'user_id_of_testuser')
    #
    # @patch('routes.user_routes.decode_clerk_token')
    # @patch('services.user_service.add_user_to_database')
    # def test_add_duplicate_user(self, mock_add_user_to_database, mock_decode_clerk_token):
    #     mock_decode_clerk_token.return_value = ('user_id_of_testuser', None)
    #     mock_add_user_to_database.side_effect = [(None, 'User with this ID or Email already exists', 409)]
    #
    #     token = generate_temp_token('user_id_of_testuser')
    #     user_data = {
    #         "user_id": "user_id_of_testuser",
    #         "email": "testuser@example.com"
    #     }
    #     headers = {'Authorization': f'Bearer {token}'}
    #
    #     response = self.client.post('/api/add-user', json=user_data, headers=headers)
    #
    #     self.assertEqual(response.status_code, 409)
    #     self.assertIn('error', response.json)
    #     self.assertEqual(response.json['error'], 'User with this ID or Email already exists')
    #
    # @patch('routes.user_routes.decode_clerk_token')
    # @patch('services.user_service.get_user_from_database')
    # def test_get_current_user(self, mock_decode_clerk_token, mock_get_user_from_database):
    #     user_data = [{'user_id': 'user_id_of_testuser', 'created_at': '2024-04-18T05:41:25.519126+00:00', 'email': 'testuser@example.com', 'user_role': 'customer_active'}]
    #     # Retrieve token to extract user_id
    #     mock_decode_clerk_token.return_value = ('user_id_of_testuser', None)
    #     # Retrieve user from database
    #     mock_get_user_from_database.return_value = (user_data, None, 200)
    #
    #     token = generate_temp_token('user_id_of_testuser')
    #
    #     headers = {'Authorization': f'Bearer {token}'}
    #     response = self.client.get('/api/get-current-user', headers=headers)
    #
    #     # Return user
    #     self.assertEqual(response.status_code, 200)
    #     self.assertDictEqual(response.json, user_data[0])
    #
    #     mock_decode_clerk_token.assert_called_once_with(token)
    #     mock_get_user_from_database.assert_called_once_with('user_id_of_testuser')
