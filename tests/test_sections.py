import sys
import os
import unittest
from unittest.mock import MagicMock, patch
from datetime import datetime

# Add the parent directory to sys.path to allow importing tornApi and sections
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from logger import setup_logger, close_logger
from tornApi import TornAPI
from sections import User, Sections

class TestUser(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """Set up the environment and logger once for all tests."""
        cls.logger, cls.file_handler = setup_logger('test_logger', 'INFO')

    @classmethod
    def tearDownClass(cls):
        """Close the logger once all tests are completed."""
        close_logger(cls.logger, cls.file_handler)

    def setUp(self):
        """Create a new TornAPI instance and Sections instance before each test."""
        self.api = MagicMock(spec=TornAPI)
        self.user_id = 123456  # Example user ID
        self.sections = Sections(self.api)
        self.user = self.sections.user(self.user_id)

    def tearDown(self):
        """Clean up after each test."""
        self.api = None
        self.user = None

    def test_user_initialization(self):
        """Test if the User is initialized correctly."""
        # Test user ID
        self.assertEqual(self.user.user_id, self.user_id)
        
        # Test API instance
        self.assertEqual(self.user.api, self.api)
        
           # Test all section initializations
        sections_to_test = [
            ('ammo', 'Ammo'),
            ('attacks', 'Attacks'),
            ('attacks_full', 'AttacksFull'),
            ('bars', 'Bars'),
            ('basic', 'Basic'),
            ('battle_stats', 'BattleStats'),
            ('bazaar', 'Bazaar'),
            ('cooldowns', 'Cooldowns'),
            ('crimes', 'Crimes'),
            ('criminal_record', 'CriminalRecord'),
            ('discord', 'Discord'),
            ('display_items', 'DisplayItems'),
            ('education', 'Education'),
            ('equipment', 'Equipment'),  # Added Equipment section
            ('events', 'Events'),        # Added Events section
            ('gym', 'Gym'),              # Added Gym section
            ('hof', 'HallOfFame'),       # Added HallOfFame section
            ('honors', 'Honors'),        # Added Honors section
            ('icons', 'Icons'),          # Added Icons section
            ('jobpoints', 'JobPoints'),   # Added JobPoints section
            ('log', 'Log'),              # Added Log section
            ('medals', 'Medals'),        # Added Medals section
            ('merits', 'Merits'),        # Added Merits section
            ('messages', 'Messages'),     # Added Messages section
            ('missions', 'Missions'),      # Added Missions section
            ('money', 'Money'),          # Added Money section
            ('networth', 'Networth'),    # Added Networth section
            ('newevents', 'NewEvents'),   # Added NewEvents section
            ('newmessages', 'NewMessages'), # Added NewMessages section
            ('notifications', 'Notifications'), # Added Notifications section
            ('perks', 'Perks'),          # Added Perks section
            ('personalstats', 'PersonalStats'), # Added PersonalStats section
            ('profile', 'Profile'),      # Added Profile section
            ('properties', 'Properties'), # Added Properties section
            ('public_status', 'PublicStatus'), # Added PublicStatus section
            ('refills', 'Refills'),      # Added Refills section
            ('reports', 'Reports'),      # Added Reports section
            ('revives', 'Revives'),      # Added Revives section
            ('revives_full', 'RevivesFull'), # Added RevivesFull section
            ('skills', 'Skills'),        # Added Skills section
            ('stocks', 'Stocks'),        # Added Stocks section
            ('timestamp', 'Timestamp'),  # Added Timestamp section
            ('travel', 'Travel'),        # Added Travel section
            ('weapon_exp', 'WeaponExp'), # Added WeaponExp section
            ('work_stats', 'WorkStats'), # Added WorkStats section
        ]
        
        for attr_name, class_name in sections_to_test:
            # Test that the attribute exists
            self.assertTrue(hasattr(self.user, attr_name), f"User missing {attr_name} attribute")
            
            # Test that the attribute is not None
            section = getattr(self.user, attr_name)
            self.assertIsNotNone(section, f"{attr_name} should not be None")
            
            # Test that the section has the correct user_id
            self.assertEqual(section.user_id, self.user_id, f"{attr_name} has incorrect user_id")
            
            # Test that the section has the correct API instance
            self.assertEqual(section.api, self.api, f"{attr_name} has incorrect API instance")
    
    def test_fetch_sections(self):
        """Test fetching data for all sections with mock responses."""
    # TODO : Needs to update the test cases to include all user test cases 
       
        test_cases = [
            {
                'section_name': 'ammo',
                'method_name': 'fetch_ammo',
                'mock_response': {
                    'ammo': [
                        {'ammoID': 1, 'equipped': 1, 'quantity': 10, 'size': 'small', 'type': 'bullet', 'typeID': 101},
                        {'ammoID': 2, 'equipped': 0, 'quantity': 5, 'size': 'large', 'type': 'shell', 'typeID': 102}
                    ]
                },
                'expected_assertions': [
                    ('len(result)', 2),
                    ('result[0].ammo_id', 1),
                    ('result[0].equipped', True),
                    ('result[0].quantity', 10),
                    ('result[1].ammo_id', 2),
                    ('result[1].equipped', False),
                    ('result[1].quantity', 5)
                ]
            },
            {
                'section_name': 'attacks',
                'method_name': 'fetch_attacks',
                'mock_response': {
                    'attacks': {
                        '1': {
                            'attacker_id': 123456,
                            'attacker_name': 'TestAttacker',
                            'defender_id': 789012,
                            'defender_name': 'TestDefender',
                            'result': 'Hospitalized',
                            'respect_gain': 3.5,
                            'timestamp_started': 1609459200,
                            'timestamp_ended': 1609459260
                        }
                    }
                },
                'expected_assertions': [
                    ('len(result)', 1),
                    ('result[0].attacker_id', 123456),
                    ('result[0].defender_name', 'TestDefender'),
                    ('result[0].result', 'Hospitalized')
                ]
            },
            {
                'section_name': 'bars',
                'method_name': 'fetch_bars',
                'mock_response': {
                    'energy': {'current': 100, 'maximum': 150, 'increment': 5, 'interval': 300, 'ticktime': 60, 'fulltime': 3000},
                    'nerve': {'current': 25, 'maximum': 100, 'increment': 1, 'interval': 300, 'ticktime': 60, 'fulltime': 22500},
                    'happy': {'current': 250, 'maximum': 250, 'increment': 1, 'interval': 300, 'ticktime': 60, 'fulltime': 0},
                    'life': {'current': 100, 'maximum': 100, 'increment': 1, 'interval': 300, 'ticktime': 60, 'fulltime': 0},
                    'chain': {'current': 10, 'maximum': 25, 'timeout': 1800, 'modifier': 1.25, 'cooldown': 0}
                },
                'expected_assertions': [
                    ('result.energy.current', 100),
                    ('result.nerve.maximum', 100),
                    ('result.happy.current', 250),
                    ('result.chain.modifier', 1.25)
                ]
            },
            {
                'section_name': 'battle_stats',
                'method_name': 'fetch_battle_stats',
                'mock_response': {
                    'strength': 1000,
                    'defense': 900,
                    'speed': 800,
                    'dexterity': 700,
                    'total': 3400,
                    'strength_modifier': 1.2,
                    'defense_modifier': 1.1,
                    'speed_modifier': 1.0,
                    'dexterity_modifier': 1.1
                },
                'expected_assertions': [
                    ('result.strength', 1000),
                    ('result.total', 3400),
                    ('result.strength_modifier', 1.2)
                ]
            },
            {
                'section_name': 'bazaar',
                'method_name': 'fetch_bazaar',
                'mock_response': {
                    'bazaar': [
                        {
                            'ID': 1,
                            'name': 'Test Item',
                            'type': 'Melee',
                            'quantity': 5,
                            'price': 1000,
                            'market_price': 1200
                        }
                    ]
                },
                'expected_assertions': [
                    ('len(result)', 1),
                    ('result[0].name', 'Test Item'),
                    ('result[0].quantity', 5),
                    ('result[0].price', 1000)
                ]
            },
            {
                'section_name': 'cooldowns',
                'method_name': 'fetch_cooldowns',
                'mock_response': {
                    'cooldowns': {
                        'drug': 3600,
                        'medical': 1800,
                        'booster': 7200
                    }
                },
                'expected_assertions': [
                    ('result.drug', 3600),
                    ('result.medical', 1800),
                    ('result.booster', 7200)
                ]
            },
            {
                'section_name': 'crimes',
                'method_name': 'fetch_crimes',
                'mock_response': {
                    'criminalrecord': {
                        'selling_illegal_products': 10,
                        'theft': 5,
                        'drug_deals': 3,
                        'computer_crimes': 2,
                        'murder': 1,
                        'fraud_crimes': 4,
                        'other': 2,
                        'total': 27
                    }
                },
                'expected_assertions': [
                    ('result.selling_illegal_products', 10),
                    ('result.theft', 5),
                    ('result.total', 27)
                ]
            },
            {
                'section_name': 'discord',
                'method_name': 'fetch_discord',
                'mock_response': {
                    'discord': {
                        'discordID': '123456789',
                        'userID': self.user_id
                    }
                },
                'expected_assertions': [
                    ('result.discord_id', '123456789'),
                    ('result.user_id', self.user_id)
                ]
            },
                        {
                'section_name': 'discord',
                'method_name': 'fetch_discord',
                'mock_response': {
                    'discord': {
                        'discordID': '123456789',
                        'userID': self.user_id
                    }
                },
                'expected_assertions': [
                    ('result.discord_id', '123456789'),
                    ('result.user_id', self.user_id)
                ]
            },
            {
                'section_name': 'display_items',
                'method_name': 'fetch_display',
                'mock_response': {
                    'display': [
                        {
                            'ID': 1,
                            'name': 'Item 1',
                            'quantity': 5,
                            'market_price': 100,
                            'circulation': 50,
                            'type': 'item',
                            'UID': 1001
                        },
                        {
                            'ID': 2,
                            'name': 'Item 2',
                            'quantity': 10,
                            'market_price': 200,
                            'circulation': 100,
                            'type': 'item',
                            'UID': 1002
                        }
                    ]
                },
                'expected_assertions': [
                    ('len(result)', 2),
                    ('result[0].name', 'Item 1'),
                    ('result[1].name', 'Item 2')
                ]
            },
            {
                'section_name': 'education',
                'method_name': 'fetch_education',
                'mock_response': {
                    'education_completed': ['Education 1', 'Education 2'],
                    'education_current': 3,
                    'education_timeleft': 10
                },
                'expected_assertions': [
                    ('result.education_completed', ['Education 1', 'Education 2']),
                    ('result.education_current', 3),
                    ('result.education_timeleft', 10)
                ]
            },
        ]

        for test_case in test_cases:
            with self.subTest(section=test_case['section_name']):
                with patch.object(self.api, 'make_request', return_value=test_case['mock_response']):
                    # Get the section instance and method
                    section = getattr(self.user, test_case['section_name'])
                    method = getattr(section, test_case['method_name'])
                    
                    # Call the method and get the result
                    result = method()
                    
                    # Verify all expected assertions
                    for assertion, expected_value in test_case['expected_assertions']:
                        actual_value = eval(assertion)
                        self.assertEqual(actual_value, expected_value, 
                            f"{test_case['section_name']}: Expected {assertion} to be {expected_value}, but got {actual_value}")
                    
                    # Verify that the API was called exactly once
                    self.api.make_request.assert_called_once()

    def test_fetch_with_no_data(self):
        """Test fetching when API returns no data for all sections."""
        # Define the sections and their expected behavior when no data is returned
        sections_to_test = [
            ('ammo', 'fetch_ammo', []),
            ('attacks', 'fetch_attacks', []),
            ('attacks_full', 'fetch_attacks_full', []),
            ('bars', 'fetch_bars', None),
            ('basic', 'fetch_basic', None),
            ('battle_stats', 'fetch_battle_stats', None),
            ('bazaar', 'fetch_bazaar', []),
            ('cooldowns', 'fetch_cooldowns', None),
            ('crimes', 'fetch_crimes', None),
            ('criminal_record', 'fetch_record', None),
            ('discord', 'fetch_discord', None),
            ('display_items', 'fetch_display', []),
            ('education', 'fetch_education', None),
            ('equipment', 'fetch_equipment', []),  # Added Equipment section
            ('events', 'fetch_events', []),          # Added Events section
            ('gym', 'fetch_gym', None),              # Added Gym section
            ('hof', 'fetch_hof', None),              # Added HallOfFame section
            ('honors', 'fetch_honors', {}),        # Added Honors section
            ('icons', 'fetch_icons', {}),          # Added Icons section
            ('jobpoints', 'fetch_jobpoints', {}),  # Added JobPoints section
            ('log', 'fetch_log', None),              # Added Log section
            ('medals', 'fetch_medals', {}),        # Added Medals section
            ('merits', 'fetch_merits', None),        # Added Merits section
            ('messages', 'fetch_messages', None),    # Added Messages section
            ('missions', 'fetch_missions', None),    # Added Missions section
            ('money', 'fetch_money', None),          # Added Money section
            ('networth', 'fetch_networth', None),    # Added Networth section
            ('newevents', 'fetch_newevents', None),     # Added NewEvents section
            ('newmessages', 'fetch_newmessages', None),  # Added NewMessages section
            ('notifications', 'fetch_notifications', None),  # Added Notifications section
            ('perks', 'fetch_perks', None),          # Added Perks section
            ('personalstats', 'fetch_personalstats', None),  # Added PersonalStats section
            ('profile', 'fetch_profile', None),      # Added Profile section
            ('properties', 'fetch_properties', None), # Added Properties section
            ('public_status', 'fetch_public_status', None), # Added PublicStatus section
            ('refills', 'fetch_refills', None),      # Added Refills section
            ('reports', 'fetch_reports', None),      # Added Reports section
            ('revives', 'fetch_revives', None),      # Added Revives section
            ('revives_full', 'fetch_latest_revives_full', []), # Added RevivesFull section
            ('skills', 'fetch_skills', None),        # Added Skills section
            ('stocks', 'fetch_stocks', None),        # Added Stocks section
            ('timestamp', 'fetch_current_timestamp', None),  # Added Timestamp section
            ('travel', 'fetch_travel_info', None),        # Added Travel section
            ('weapon_exp', 'fetch_weapon_exp', None), # Added WeaponExp section
            ('work_stats', 'fetch_work_stats', None), # Added WorkStats section
        ]
    
        # Set up the API to return empty data
        self.api.make_request.return_value = {}
        
        for attr_name, method_name, expected_result in sections_to_test:
            with self.subTest(section=attr_name):
                # Get the section instance
                section = getattr(self.user, attr_name)
                
                # Get the fetch method
                fetch_method = getattr(section, method_name)
                
                # Call the fetch method and check the result
                result = fetch_method()
                
                # Use appropriate assertion based on expected result type
                if expected_result is None:
                    self.assertIsNone(result, 
                        f"{attr_name}.{method_name}() should return None when no data is available")
                else:
                    self.assertEqual(result, expected_result,
                        f"{attr_name}.{method_name}() should return {expected_result} when no data is available")
                
                # Verify that the API was called
                self.api.make_request.assert_called()
                self.api.make_request.reset_mock()

if __name__ == '__main__':
    unittest.main(verbosity=2)