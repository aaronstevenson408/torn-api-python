import unittest
from unittest.mock import patch
import time
from rate_limiter import RateLimiter  # Ensure you import the RateLimiter class

class TestRateLimiter(unittest.TestCase):
    def setUp(self):
        """Set up a RateLimiter instance for testing."""
        self.limiter = RateLimiter(limit=5, timeframe=10)  # Allow 5 requests in 10 seconds

    @patch('time.time')
    def test_request_allowed_initially(self, mock_time):
        """Test that requests are allowed initially."""
        mock_time.return_value = 0  # Mock the current time to 0
        self.assertTrue(self.limiter.request_allowed())

    @patch('time.time')
    def test_limit_not_exceeded(self, mock_time):
        """Test that requests are allowed until the limit is reached."""
        mock_time.return_value = 0  # Start at time 0
        for i in range(5):  # Make 5 requests
            self.assertTrue(self.limiter.request_allowed())
            self.limiter.log_request()
            mock_time.return_value += 1  # Simulate passing time after each request

    @patch('time.time')
    def test_limit_exceeded(self, mock_time):
        """Test that the limit is exceeded after 5 requests."""
        mock_time.return_value = 0  # Mock the current time
        for _ in range(5):  # Make 5 requests
            self.limiter.log_request()
            mock_time.return_value += 1  # Simulate passing time
        
        # The next request should be denied
        self.assertFalse(self.limiter.request_allowed())

    @patch('time.time')
    def test_cleanup_functionality(self, mock_time):
        """Test that old requests are cleaned up after the timeframe."""
        mock_time.return_value = 0  # Start at time 0
        for _ in range(5):  # Make 5 requests
            self.limiter.log_request()
            mock_time.return_value += 1  # Simulate passing time
        
        # Now we simulate the passage of time beyond the timeframe
        mock_time.return_value += 10  # Fast-forward time by 10 seconds
        
        # Now requests should be allowed again
        self.assertTrue(self.limiter.request_allowed())

    @patch('time.time')
    def test_logging_after_limit_exceeded(self, mock_time):
        """Test that logging a request after exceeding the limit raises an error."""
        mock_time.return_value = 0  # Mock the current time
        for _ in range(5):  # Make 5 requests
            self.limiter.log_request()
            mock_time.return_value += 1  # Simulate passing time
        
        with self.assertRaises(Exception) as context:
            self.limiter.log_request()  # This should raise an exception

        self.assertEqual(str(context.exception), "Request limit exceeded")

if __name__ == '__main__':
    unittest.main()
