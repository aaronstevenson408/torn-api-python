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
logger, file_handler = setup_logger('Test_Markets', env['DEBUG_LEVEL'])

class TestMarket(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """Set up the environment and logger once for all tests."""
        cls.logger, cls.file_handler = setup_logger('test_logger', 'INFO')

    @classmethod
    def tearDownClass(cls):
        """Close the logger once all tests are completed."""
        close_logger(cls.logger, cls.file_handler)

    def setUp(self):
        """Create a new TornAPI instance and Market instance before each test."""
        self.api = MagicMock(spec=TornAPI)
        self.sections = Sections(self.api)
        self.item_id = 789012  # Example item ID
        self.market = self.sections.market(self.item_id)
        
    def tearDown(self):
        """Clean up after each test."""
        self.api = None
        self.item_id = None
        self.market = None

    def test_market_initialization(self):
        """Test if the Market is initialized correctly."""
        self.assertEqual(self.market.item_id, self.item_id)
        self.assertEqual(self.market.api, self.api)
        
        # Test all section initializations
        sections_to_test = [
            ('bazaar', 'Bazaar'),
            ('itemmarket', 'ItemMarket'),
            ('lookup', 'Lookup'),
            ('pointsmarket', 'PointsMarket'),
            ('timestamp', 'Timestamp')
        ]
        
        for attr_name, class_name in sections_to_test:
            self.assertTrue(hasattr(self.market, attr_name), f"Market missing {attr_name} attribute")
            section = getattr(self.market, attr_name)
            self.assertIsNotNone(section, f"{attr_name} should not be None")
            if hasattr(section, 'item_id'):
                self.assertEqual(section.item_id, self.item_id, f"{attr_name} has incorrect item_id")
            self.assertEqual(section.api, self.api, f"{attr_name} has incorrect API instance")

    # ----- Bazaar Tests -----

    def test_fetch_bazaar_data(self):
        """Test fetching bazaar data with valid mock response."""
        mock_response = {
            'bazaar': [
                {'cost': 500, 'quantity': 10},
                {'cost': 750, 'quantity': 5}
            ]
        }

        with patch.object(self.api, 'make_request', return_value=mock_response):
            result = self.market.bazaar.fetch_data()
            
            self.assertIsNotNone(result)
            self.assertEqual(len(result.bazaar), 2)
            self.assertEqual(result.bazaar[0].cost, 500)
            self.assertEqual(result.bazaar[0].quantity, 10)
            self.api.make_request.assert_called_once_with('market', self.item_id, 'bazaar')

    def test_fetch_bazaar_with_no_data(self):
        """Test fetching bazaar data when API returns no data."""
        self.api.make_request.return_value = {}
        
        result = self.market.bazaar.fetch_data()
        
        self.assertIsNone(result)
        self.api.make_request.assert_called_once_with('market', self.item_id, 'bazaar')

    def test_fetch_bazaar_with_api_error(self):
        """Test fetching bazaar data when API raises an exception."""
        self.api.make_request.side_effect = Exception("API Error")
        
        result = self.market.bazaar.fetch_data()
        
        self.assertIsNone(result)
        self.api.make_request.assert_called_once_with('market', self.item_id, 'bazaar')

    def test_bazaar_data_initialization(self):
        """Test the initialization of BazaarData class."""
        mock_data = {
            'bazaar': [
                {'cost': 500, 'quantity': 10},
                {'cost': 750, 'quantity': 5}
            ]
        }
        
        bazaar_data = self.market.bazaar.BazaarData(mock_data)
        
        self.assertEqual(len(bazaar_data.bazaar), 2)
        self.assertEqual(bazaar_data.bazaar[0].cost, 500)
        self.assertEqual(bazaar_data.bazaar[0].quantity, 10)

    def test_bazaar_data_initialization_with_missing_data(self):
        """Test the initialization of BazaarData class with missing bazaar data."""
        mock_data = {}  # Empty dictionary to simulate missing data
        
        bazaar_data = self.market.bazaar.BazaarData(mock_data)
        
        self.assertEqual(len(bazaar_data.bazaar), 0)

    # ----- ItemMarket Tests -----

    def test_fetch_itemmarket_data(self):
        """Test fetching item market data with valid mock response."""
        mock_response = {
            'itemmarket': [
                {'cost': 1500, 'quantity': 3},
                {'cost': 2000, 'quantity': 2}
            ]
        }

        with patch.object(self.api, 'make_request', return_value=mock_response):
            result = self.market.itemmarket.fetch_data()
            
            self.assertIsNotNone(result)
            self.assertEqual(len(result.itemmarket), 2)
            self.assertEqual(result.itemmarket[0].cost, 1500)
            self.assertEqual(result.itemmarket[0].quantity, 3)
            self.api.make_request.assert_called_once_with('market', self.item_id, 'itemmarket')

    def test_fetch_itemmarket_with_no_data(self):
        """Test fetching item market data when API returns no data."""
        self.api.make_request.return_value = {}
        
        result = self.market.itemmarket.fetch_data()
        
        self.assertIsNone(result)
        self.api.make_request.assert_called_once_with('market', self.item_id, 'itemmarket')

    def test_fetch_itemmarket_with_api_error(self):
        """Test fetching item market data when API raises an exception."""
        self.api.make_request.side_effect = Exception("API Error")
        
        result = self.market.itemmarket.fetch_data()
        
        self.assertIsNone(result)
        self.api.make_request.assert_called_once_with('market', self.item_id, 'itemmarket')

    def test_itemmarket_data_initialization(self):
        """Test the initialization of ItemMarketData class."""
        mock_data = {
            'itemmarket': [
                {'cost': 1500, 'quantity': 3},
                {'cost': 2000, 'quantity': 2}
            ]
        }
        
        itemmarket_data = self.market.itemmarket.ItemMarketData(mock_data)
        
        self.assertEqual(len(itemmarket_data.itemmarket), 2)
        self.assertEqual(itemmarket_data.itemmarket[0].cost, 1500)
        self.assertEqual(itemmarket_data.itemmarket[0].quantity, 3)

    def test_itemmarket_data_initialization_with_missing_data(self):
        """Test the initialization of ItemMarketData class with missing data."""
        mock_data = {}  # Empty dictionary to simulate missing data
        
        itemmarket_data = self.market.itemmarket.ItemMarketData(mock_data)
        
        self.assertEqual(len(itemmarket_data.itemmarket), 0)

    # ----- Lookup Tests -----

    def test_fetch_lookup_data(self):
        """Test fetching lookup data with valid mock response."""
        mock_response = {
            'selections': ['SelectionA', 'SelectionB', 'SelectionC']
        }

        with patch.object(self.api, 'make_request', return_value=mock_response):
            result = self.market.lookup.fetch_data()
            
            self.assertIsNotNone(result)
            self.assertEqual(result.selections, ['SelectionA', 'SelectionB', 'SelectionC'])
            self.api.make_request.assert_called_once_with('market', '', 'lookup')

    def test_fetch_lookup_with_no_data(self):
        """Test fetching lookup data when API returns no data."""
        self.api.make_request.return_value = {}
        
        result = self.market.lookup.fetch_data()
        
        self.assertIsNone(result)
        self.api.make_request.assert_called_once_with('market', '', 'lookup')

    def test_fetch_lookup_with_api_error(self):
        """Test fetching lookup data when API raises an exception."""
        self.api.make_request.side_effect = Exception("API Error")
        
        result = self.market.lookup.fetch_data()
        
        self.assertIsNone(result)
        self.api.make_request.assert_called_once_with('market', '', 'lookup')

    def test_lookup_data_initialization(self):
        """Test the initialization of LookupData class."""
        mock_data = {
            'selections': ['SelectionA', 'SelectionB', 'SelectionC']
        }
        
        lookup_data = self.market.lookup.LookupData(mock_data)
        
        self.assertEqual(lookup_data.selections, ['SelectionA', 'SelectionB', 'SelectionC'])

    def test_lookup_data_initialization_with_missing_data(self):
        """Test the initialization of LookupData class with missing selections."""
        mock_data = {}  # Empty dictionary to simulate missing data
        
        lookup_data = self.market.lookup.LookupData(mock_data)
        
        self.assertEqual(lookup_data.selections, [])

    # ----- PointsMarket Tests -----

    def test_fetch_pointsmarket_data(self):
        """Test fetching points market data with valid mock response."""
        mock_response = {
            'pointsmarket': {
                '1': {'cost': 300, 'quantity': 20, 'total_cost': 6000},
                '2': {'cost': 450, 'quantity': 15, 'total_cost': 6750}
            }
        }

        with patch.object(self.api, 'make_request', return_value=mock_response):
            result = self.market.pointsmarket.fetch_data()
            
            self.assertIsNotNone(result)
            self.assertEqual(len(result.points), 2)
            self.assertEqual(result.points['1'].cost, 300)
            self.assertEqual(result.points['1'].quantity, 20)
            self.assertEqual(result.points['1'].total_cost, 6000)
            self.api.make_request.assert_called_once_with('market', '', 'pointsmarket')

    def test_fetch_pointsmarket_with_no_data(self):
        """Test fetching points market data when API returns no data."""
        self.api.make_request.return_value = {}
        
        result = self.market.pointsmarket.fetch_data()
        
        self.assertIsNone(result)
        self.api.make_request.assert_called_once_with('market', '', 'pointsmarket')

    def test_fetch_pointsmarket_with_api_error(self):
        """Test fetching points market data when API raises an exception."""
        self.api.make_request.side_effect = Exception("API Error")
        
        result = self.market.pointsmarket.fetch_data()
        
        self.assertIsNone(result)
        self.api.make_request.assert_called_once_with('market', '', 'pointsmarket')

    def test_pointsmarket_data_initialization(self):
        """Test the initialization of PointsMarketData class."""
        mock_data = {
            '1': {'cost': 300, 'quantity': 20, 'total_cost': 6000},
            '2': {'cost': 450, 'quantity': 15, 'total_cost': 6750}
        }
        
        pointsmarket_data = self.market.pointsmarket.PointsMarketData(mock_data)
        
        self.assertEqual(len(pointsmarket_data.points), 2)
        self.assertEqual(pointsmarket_data.points['1'].cost, 300)
        self.assertEqual(pointsmarket_data.points['1'].quantity, 20)
        self.assertEqual(pointsmarket_data.points['1'].total_cost, 6000)

    def test_pointsmarket_data_initialization_with_missing_data(self):
        """Test the initialization of PointsMarketData class with missing points data."""
        mock_data = {}  # Empty dictionary to simulate missing data
        
        pointsmarket_data = self.market.pointsmarket.PointsMarketData(mock_data)
        
        self.assertEqual(len(pointsmarket_data.points), 0)

    # ----- Timestamp Tests -----

    def test_fetch_timestamp(self):
        """Test fetching timestamp with valid mock response."""
        mock_response = {
            'timestamp': 1632968400
        }

        with patch.object(self.api, 'make_request', return_value=mock_response):
            result = self.market.timestamp.fetch_data()
            
            self.assertIsNotNone(result)
            self.assertEqual(result, 1632968400)
            self.api.make_request.assert_called_once_with('market', '', 'timestamp')

    def test_fetch_timestamp_with_no_data(self):
        """Test fetching timestamp when API returns no data."""
        self.api.make_request.return_value = {}
        
        result = self.market.timestamp.fetch_data()
        
        self.assertIsNone(result)
        self.api.make_request.assert_called_once_with('market', '', 'timestamp')

    def test_fetch_timestamp_with_api_error(self):
        """Test fetching timestamp when API raises an exception."""
        self.api.make_request.side_effect = Exception("API Error")
        
        result = self.market.timestamp.fetch_data()
        
        self.assertIsNone(result)
        self.api.make_request.assert_called_once_with('market', '', 'timestamp')

    def test_timestamp_representation(self):
        """Test the string representation of Timestamp."""
        self.market.timestamp.data = 1632968400
        self.assertEqual(str(self.market.timestamp), "Timestamp(timestamp=1632968400)")

    def test_timestamp_repr(self):
        """Test the repr of Timestamp."""
        self.market.timestamp.data = 1632968400
        self.assertEqual(repr(self.market.timestamp), "Timestamp(timestamp=1632968400)")

if __name__ == '__main__':
    unittest.main(verbosity=2)