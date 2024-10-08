import unittest
from unittest.mock import patch, MagicMock
import sys
import os
import requests

# Add the parent directory to sys.path to allow importing tornApi
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tornApi import TornAPI

class TestTornAPI(unittest.TestCase):
    @patch('tornApi.load_environment_variables')
    @patch('tornApi.setup_logger')
    def setUp(self, mock_setup_logger, mock_load_env):
        self.mock_env = {
            'API_KEYS': {'full': 'test_api_key'},
            'DEBUG_LEVEL': 'INFO'
        }
        mock_load_env.return_value = self.mock_env
        mock_setup_logger.return_value = (MagicMock(), MagicMock())
        self.api = TornAPI(access_level='full')

    def tearDown(self):
        self.api.close()

    def test_torn_api_initialization(self):
        self.assertEqual(self.api.api_key, 'test_api_key')
        self.assertIsNotNone(self.api.logger)

    @patch('tornApi.load_environment_variables')
    @patch('tornApi.setup_logger')
    def test_torn_api_initialization_invalid_access_level(self, mock_setup_logger, mock_load_env):
        mock_env = {'API_KEYS': {}, 'DEBUG_LEVEL': 'INFO'}
        mock_load_env.return_value = mock_env
        mock_setup_logger.return_value = (MagicMock(), MagicMock())
        with self.assertRaises(ValueError) as context:
            TornAPI(access_level='invalid')
        self.assertIn("API key is required for the specified access level", str(context.exception))

    def test_interpret_error(self):
        test_cases = [
            (0, "Unknown error. An unhandled error has occurred."),
            (1, "Key is empty. Please provide a valid API key."),
            (2, "Incorrect key. The provided API key is invalid."),
            (5, "Too many requests. Requests are blocked due to exceeding the limit."),
            (999, "Unknown error code. Please check the API documentation.")
        ]
        for error_code, expected_message in test_cases:
            with self.subTest(error_code=error_code):
                self.assertEqual(self.api.interpret_error(error_code), expected_message)

    @patch('tornApi.requests.get')
    def test_make_request_success(self, mock_get):
        mock_response = MagicMock()
        mock_response.json.return_value = {"success": True, "data": "test_data"}
        mock_response.status_code = 200
        mock_get.return_value = mock_response

        result = self.api.make_request('user', '123', 'basic,stats', {'extra_param': 'value'})

        self.assertEqual(result, {"success": True, "data": "test_data"})
        
        # Get the actual URL from the call args
        actual_url = mock_get.call_args[0][0]  # Get the actual URL from the call args
        
        # Check if the actual URL contains the expected parameters
        self.assertIn('selections=basic%2Cstats', actual_url)  # URL-encoded comma
        self.assertIn('key=test_api_key', actual_url)
        self.assertIn('extra_param=value', actual_url)


    @patch('tornApi.requests.get')
    def test_make_request_api_error(self, mock_get):
        mock_response = MagicMock()
        mock_response.json.return_value = {"error": {"code": 2}}
        mock_response.status_code = 400
        mock_get.return_value = mock_response

        result = self.api.make_request('user', '123', 'basic,stats')

        self.assertIsNone(result)

    @patch('tornApi.requests.get')
    def test_make_request_network_error(self, mock_get):
        mock_get.side_effect = requests.exceptions.RequestException("Network error")

        result = self.api.make_request('user', '123', 'basic,stats')

        self.assertIsNone(result)

    @patch('tornApi.RateLimiter.request_allowed')
    def test_make_request_rate_limit_exceeded(self, mock_request_allowed):
        mock_request_allowed.return_value = False

        result = self.api.make_request('user', '123', 'basic,stats')

        self.assertIsNone(result)

if __name__ == '__main__':
    unittest.main()
