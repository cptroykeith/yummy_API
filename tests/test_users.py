import unittest
from unittest.mock import patch, Mock

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from server import db
from users.models import User
from users.service import create_user
from utils.common import generate_response
from utils.http_code import HTTP_201_CREATED

class CreateUserTestCase(unittest.TestCase):

    def setUp(self):
        # Create a Flask application
        self.app = Flask(__name__)
        self.app.config['TESTING'] = True
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

        # Initialize the database
        db.init_app(self.app)
        with self.app.app_context():
            db.create_all()

        # Create a test client
        self.client = self.app.test_client()

    def tearDown(self):
        # Remove the database tables and close the app context
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    # @patch('utils.common.generate_response')
    # def test_create_user_with_errors(self, mock_generate_response):
    #     with self.app.test_request_context():
    #         input_data = {
    #             # Invalid input data to trigger errors
    #             "username": "",  # Invalid username
    #             "email": "test@example.com",
    #             "password": "password123"
    #         }

    #         response = create_user(None, input_data)

    #         mock = Mock()
    #         mock.generate_response = generate_response
    #         # Check that the generate_response function was called with the expected arguments
    #         mock.generate_response.assert_called_once_with(
    #             message={'username': 'Field may not be blank'},
    #             status=400
    #         )

    @patch('utils.common.generate_response')
    def test_create_user_success(self, mock_generate_response):
        with self.app.test_request_context():
            input_data = {
                "username": "testuser",
                "email": "test@example.com",
                "password": "password123"
            }

            # Simulating a successful database operation
            with patch.object(db.session, 'commit'):
                response = create_user(None, input_data)

            # Check that the User instance is created and added to the database
            print('this is response', response)
            print (len(response))
            self.assertIsInstance(response, tuple)  # Check for tuple instead of dict
            self.assertEqual(response[0].get('message'), 'User Created')  # Check status in the tuple instead of response[0]['status']
            # self.assertIn(response[0]['status'], HTTP_201_CREATED)  # Check message in the tuple instead of response[0]['message']

            # mock = Mock()
            # mock.generate_response = generate_response
            # # Check that the generate_response function was called with the expected arguments
            # mock.generate_response.assert_called_once_with(
            #     data={'username': 'testuser', 'email': 'test@example.com'},
            #     message='User Created',
            #     status=HTTP_201_CREATED
            # )


    # @patch('utils.common.generate_response')
    # def test_create_user_duplicate_username(self, mock_generate_response):
    #     with self.app.test_request_context():
    #         # Simulating a duplicate username scenario
    #         input_data = {
    #             "username": "existinguser",
    #             "email": "test@example.com",
    #             "password": "password123"
    #         }
    #         existing_user = User(username="existinguser", email="test@example.com")
    #         with patch.object(db.session.query(User), 'first') as mock_query:
    #             mock_query.return_value = existing_user
    #             response = create_user(None, input_data)

    #         mock = Mock()
    #         mock.generate_response = generate_response
    #         # Check that the generate_response function was called with the expected arguments
    #         mock.generate_response.assert_called_once_with(
    #             message='Username already exists',
    #             status=400
    #         )

if __name__ == '__main__':
    unittest.main()
