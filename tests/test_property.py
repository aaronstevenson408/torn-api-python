import sys
import os
import unittest
from unittest.mock import MagicMock, patch
from datetime import datetime
# Add the parent directory to sys.path to allow importing tornApi and sections
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from logger import setup_logger, close_logger
from tornApi import TornAPI
from sections import Sections
from env_loader import load_environment_variables

env = load_environment_variables()
if env is None:
    raise ValueError("Failed to load environment variables.")
logger, file_handler = setup_logger('Test_Properties', env['DEBUG_LEVEL'])

class TestProperties(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """Set up the environment and logger once for all tests."""
        cls.logger, cls.file_handler = setup_logger('test_logger', 'INFO')

    @classmethod
    def tearDownClass(cls):
        """Close the logger once all tests are completed."""
        close_logger(cls.logger, cls.file_handler)

    def setUp(self):
        """Create a new TornAPI instance and Property instance before each test."""
        self.api = MagicMock(spec=TornAPI)
        self.sections = Sections(self.api)
        self.property_id = 123456  # Example property ID
        self.property = self.sections.property(self.property_id)
        
    def tearDown(self):
        """Clean up after each test."""
        self.api = None
        self.property_id = None
        self.property = None
        
    def test_property_initialization(self):
        """Test if the property is initialized correctly."""
        self.assertEqual(self.property.property_id, self.property_id)
        self.assertEqual(self.property.api, self.api)
        
        # Test all section initializations
        sections_to_test = [
            ('property', 'Property'),
            ('lookup', 'Lookup'),
            ('timestamp', 'Timestamp')
        ]
        
        for attr_name, class_name in sections_to_test:
            self.assertTrue(hasattr(self.property, attr_name), f"Property missing {attr_name} attribute")
            section = getattr(self.property, attr_name)
            self.assertIsNotNone(section, f"{attr_name} should not be None")
            self.assertEqual(section.property_id, self.property_id, f"{attr_name} has incorrect property_id")
            self.assertEqual(section.api, self.api, f"{attr_name} has incorrect API instance")
    
    def test_fetch_data(self):
        """Test fetching data for the property with mock responses."""
        mock_response = {
            'happy': 100,
            'owner_id': 5678,
            'property_type': 'House',
            'rented': {
                'cost_per_day': 1000,
                'days_left': 30,
                'total_cost': 30000,
                'user_id': 9876
            },
            'staff': ['Maid', 'Butler'],
            'upgrades': ['Pool', 'Garden'],
            'upkeep': 500,
            'users_living': 2
        }
        
        with patch.object(self.api, 'make_request', return_value=mock_response):
            result = self.property.property.fetch_data()
            
            self.assertIsNotNone(result)
            self.assertEqual(result.happy, 100)
            self.assertEqual(result.owner_id, 5678)
            self.assertEqual(result.property_type, 'House')
            self.assertEqual(result.rented.cost_per_day, 1000)
            self.assertEqual(result.rented.days_left, 30)
            self.assertEqual(result.rented.total_cost, 30000)
            self.assertEqual(result.rented.user_id, 9876)
            self.assertEqual(result.staff, ['Maid', 'Butler'])
            self.assertEqual(result.upgrades, ['Pool', 'Garden'])
            self.assertEqual(result.upkeep, 500)
            self.assertEqual(result.users_living, 2)
            
            self.api.make_request.assert_called_once_with('property', self.property_id)

    def test_fetch_data(self):
        """Test fetching when API returns no data for the property."""
        self.api.make_request.return_value = {}
        
        result = self.property.property.fetch_data()
        
        self.assertIsNone(result)
        self.api.make_request.assert_called_once_with('property', self.property_id)

    def test_fetch_data(self):
        """Test fetching when API raises an exception."""
        self.api.make_request.side_effect = Exception("API Error")
        
        result = self.property.property.fetch_data()
        
        self.assertIsNone(result)
        self.api.make_request.assert_called_once_with('property', self.property_id)

    def test_property_data_initialization(self):
        """Test the initialization of PropertyData class."""
        mock_data = {
            'happy': 100,
            'owner_id': 5678,
            'property_type': 'House',
            'rented': {
                'cost_per_day': 1000,
                'days_left': 30,
                'total_cost': 30000,
                'user_id': 9876
            },
            'staff': ['Maid', 'Butler'],
            'upgrades': ['Pool', 'Garden'],
            'upkeep': 500,
            'users_living': 2
        }
        
        property_data = self.property.property.PropertyData(mock_data)
        
        self.assertEqual(property_data.happy, 100)
        self.assertEqual(property_data.owner_id, 5678)
        self.assertEqual(property_data.property_type, 'House')
        self.assertEqual(property_data.rented.cost_per_day, 1000)
        self.assertEqual(property_data.rented.days_left, 30)
        self.assertEqual(property_data.rented.total_cost, 30000)
        self.assertEqual(property_data.rented.user_id, 9876)
        self.assertEqual(property_data.staff, ['Maid', 'Butler'])
        self.assertEqual(property_data.upgrades, ['Pool', 'Garden'])
        self.assertEqual(property_data.upkeep, 500)
        self.assertEqual(property_data.users_living, 2)

    def test_property_data_initialization_with_missing_data(self):
        """Test the initialization of PropertyData class with missing data."""
        mock_data = {}  # Empty dictionary to simulate missing data
        
        property_data = self.property.property.PropertyData(mock_data)
        
        self.assertEqual(property_data.happy, 0)
        self.assertEqual(property_data.owner_id, 0)
        self.assertEqual(property_data.property_type, 0)
        self.assertEqual(property_data.rented.cost_per_day, 0)
        self.assertEqual(property_data.rented.days_left, 0)
        self.assertEqual(property_data.rented.total_cost, 0)
        self.assertEqual(property_data.rented.user_id, 0)
        self.assertEqual(property_data.staff, [])
        self.assertEqual(property_data.upgrades, [])
        self.assertEqual(property_data.upkeep, 0)
        self.assertEqual(property_data.users_living, 0)

    def test_lookup_fetch_data(self):
        """Test fetching selections for the property."""
        mock_response = {
            'selections': ['Selection1', 'Selection2', 'Selection3']
        }
        
        with patch.object(self.api, 'make_request', return_value=mock_response):
            result = self.property.lookup.fetch_data()
            
            self.assertIsInstance(result, self.property.lookup.LookupData)
            self.assertEqual(result.selections, ['Selection1', 'Selection2', 'Selection3'])
            self.api.make_request.assert_called_once_with('property', '', 'lookup')

    def test_lookup_fetch_data(self):
        """Test fetching selections when API returns no data."""
        self.api.make_request.return_value = {}
        
        result = self.property.lookup.fetch_data()
        
        self.assertIsNone(result)
        self.api.make_request.assert_called_once_with('property', '', 'lookup')

    def test_timestamp_fetch_data(self):
        """Test fetching current timestamp for the property."""
        mock_response = {
            'timestamp': 1632968400
        }
        
        with patch.object(self.api, 'make_request', return_value=mock_response):
            result = self.property.timestamp.fetch_data()
            
            self.assertIsInstance(result, self.property.timestamp.TimestampData)
            self.assertEqual(result.timestamp, 1632968400)
            self.api.make_request.assert_called_once_with('property', self.property_id, 'timestamp')

    def test_timestamp_fetch_data(self):
        """Test fetching current timestamp when API returns no data."""
        self.api.make_request.return_value = {}
        
        result = self.property.timestamp.fetch_data()
        
        self.assertIsNone(result)
        self.api.make_request.assert_called_once_with('property', self.property_id, 'timestamp')

if __name__ == '__main__':
    unittest.main(verbosity=2)
