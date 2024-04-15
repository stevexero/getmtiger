import pytest
from flask_testing import TestCase
from app import create_app


class MyTest(TestCase):
    def create_app(self):
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
        user_data = {
            "user_id": "testuser",
            "email": "testuser@example.com"
        }
        response = self.client.post('/api/add-user', json=user_data)
        self.assertEqual(response.status_code, 201)
