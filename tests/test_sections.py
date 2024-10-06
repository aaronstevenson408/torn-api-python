import sys
import os
import unittest
from unittest.mock import MagicMock, patch
from datetime import datetime
from test_user import TestUser
from test_property import TestProperties
from test_market import TestMarket
# Add the parent directory to sys.path to allow importing tornApi and sections
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from logger import setup_logger, close_logger
from tornApi import TornAPI
from sections import Sections
from env_loader import load_environment_variables


env = load_environment_variables()
if env is None:
    raise ValueError("Failed to load environment variables.")
logger, file_handler = setup_logger('Test_Sections', env['DEBUG_LEVEL'])

if __name__ == '__main__':
    unittest.main(verbosity=2)