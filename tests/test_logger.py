import unittest
import logging
import os
from logger import setup_logger, close_logger

class TestLogger(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """Set up logger for testing."""
        cls.log, cls.file_handler = setup_logger('test_logger', level=logging.DEBUG)
        cls.log_file_path = os.path.join('logs', 'test_logger.log')

    @classmethod
    def tearDownClass(cls):
        """Remove the log file after tests."""
        close_logger(cls.log, cls.file_handler)
        if os.path.exists(cls.log_file_path):
            os.remove(cls.log_file_path)

    def test_logging_debug(self):
        """Test debug logging."""
        self.log.debug("This is a debug message.")
        with open(self.log_file_path, 'r') as f:
            logs = f.read()
        self.assertIn("This is a debug message.", logs)

    def test_logging_info(self):
        """Test info logging."""
        self.log.info("This is an info message.")
        with open(self.log_file_path, 'r') as f:
            logs = f.read()
        self.assertIn("This is an info message.", logs)

    def test_logging_warning(self):
        """Test warning logging."""
        self.log.warning("This is a warning message.")
        with open(self.log_file_path, 'r') as f:
            logs = f.read()
        self.assertIn("This is a warning message.", logs)

    def test_logging_error(self):
        """Test error logging."""
        self.log.error("This is an error message.")
        with open(self.log_file_path, 'r') as f:
            logs = f.read()
        self.assertIn("This is an error message.", logs)

    def test_logging_critical(self):
        """Test critical logging."""
        self.log.critical("This is a critical message.")
        with open(self.log_file_path, 'r') as f:
            logs = f.read()
        self.assertIn("This is a critical message.", logs)

if __name__ == "__main__":
    unittest.main()
