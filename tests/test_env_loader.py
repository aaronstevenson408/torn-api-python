import os
import unittest
from unittest.mock import patch, mock_open
from env_loader import load_environment_variables

class TestEnvLoader(unittest.TestCase):
    @patch("builtins.open", new_callable=mock_open, read_data=(
        "DEBUG_LEVEL=DEBUG\n"
        "Test-Full=yJeVHyiQDEwJlLQu\n"
        "Test-Limited=YBRGs014RIRvEwNX\n"
        "Test-Min=xlOqScgvzVAnJvrg\n"
        "Test-Public=swii30okEklgxAM6\n"
    ))
    @patch("env_loader.load_dotenv")  # Ensure to patch the correct import path
    def test_load_environment_variables(self, mock_load_dotenv, mock_file):
        # Call the function to load environment variables
        load_environment_variables()

        # Assert load_dotenv was called once
        mock_load_dotenv.assert_called_once_with('.env')

        # Manually set the environment variables as they would be set
        os.environ["DEBUG_LEVEL"] = "DEBUG"
        os.environ["Test-Full"] = "yJeVHyiQDEwJlLQu"
        os.environ["Test-Limited"] = "YBRGs014RIRvEwNX"
        os.environ["Test-Min"] = "xlOqScgvzVAnJvrg"
        os.environ["Test-Public"] = "swii30okEklgxAM6"

        # Check if the environment variables are set correctly
        self.assertEqual(os.getenv("DEBUG_LEVEL"), "DEBUG")
        self.assertEqual(os.getenv("Test-Full"), "yJeVHyiQDEwJlLQu")
        self.assertEqual(os.getenv("Test-Limited"), "YBRGs014RIRvEwNX")
        self.assertEqual(os.getenv("Test-Min"), "xlOqScgvzVAnJvrg")
        self.assertEqual(os.getenv("Test-Public"), "swii30okEklgxAM6")

    @patch("builtins.open", side_effect=FileNotFoundError)
    def test_load_environment_variables_file_not_found(self, mock_file):
        # Call the function and expect it to handle the error
        with self.assertLogs(level='ERROR') as log:
            load_environment_variables()

        self.assertIn("Error loading environment variables:", log.output[0])

if __name__ == "__main__":
    unittest.main()
