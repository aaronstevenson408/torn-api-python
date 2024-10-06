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
logger, file_handler = setup_logger('Test_User', env['DEBUG_LEVEL'])

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
        self.user_id = "123456"  # Example user ID
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
                'method_name': 'fetch_data',
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
                'method_name': 'fetch_data',
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
                'method_name': 'fetch_data',
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
                'method_name': 'fetch_data',
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
                'method_name': 'fetch_data',
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
                'method_name': 'fetch_data',
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
                'method_name': 'fetch_data',
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
                'method_name': 'fetch_data',
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
                'method_name': 'fetch_data',
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
                'method_name': 'fetch_data',
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
                'method_name': 'fetch_data',
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
            {
                'section_name': 'equipment',  # Name of the section (e.g., 'ammo', 'attacks')
                'method_name': 'fetch_data',  # Method to fetch data for the section (e.g., 'fetch_data')
                'mock_response': {
                    'equipment': [
                        {
                            'equipped': 1,
                            'ID': 123456,
                            'market_price': 10000,
                            'name': 'Kevlar Vest',
                            'quantity': 1,
                            'type': 'armor',
                            'UID': 987654
                        },
                        {
                            'equipped': 0,
                            'ID': 654321,
                            'market_price': 5000,
                            'name': 'Steel Helmet',
                            'quantity': 1,
                            'type': 'helmet',
                            'UID': 123987
                        }
                    ]
                },  # Simulated API response data for testing purposes
                'expected_assertions': [
                    ('result[0].id', 123456),
                    ('result[0].name', 'Kevlar Vest'),
                    ('result[0].market_price', 10000),
                    ('result[0].quantity', 1),
                    ('result[0].type', 'armor'),
                    ('result[0].uid', 987654),
                    ('result[1].id', 654321),
                    ('result[1].name', 'Steel Helmet'),
                    ('result[1].market_price', 5000),
                    ('result[1].quantity', 1),
                    ('result[1].type', 'helmet'),
                    ('result[1].uid', 123987)
                ]  # List of assertions to check the result after processing the mock_response
            },   
            {
                'section_name': 'events',
                'method_name': 'fetch_data',
                'mock_response': {
                    'events': {
                        'abc123': {
                            'event': 'You received a new message',
                            'timestamp': 1635018900
                        },
                        'xyz789': {
                            'event': 'You were attacked by Player123',
                            'timestamp': 1635020000
                        }
                    }
                },
                'expected_assertions': [
                    ('result[0].uuid', 'abc123'),
                    ('result[0].event', 'You received a new message'),
                    ('result[0].timestamp', 1635018900),
                    ('result[1].uuid', 'xyz789'),
                    ('result[1].event', 'You were attacked by Player123'),
                    ('result[1].timestamp', 1635020000)
                ]
            },
            {
                'section_name': 'gym',
                'method_name': 'fetch_data',
                'mock_response': {
                    'active_gym': 'Supreme Gym'
                },
                'expected_assertions': [
                    ('result', 'Supreme Gym')
                ]
            },
            {
                'section_name': 'hof',
                'method_name': 'fetch_data',
                'mock_response': {
                    'halloffame': {
                        'strength': {'rank': 5, 'value': 10000},
                        'speed': {'rank': 12, 'value': 8500}
                    }
                },
                'expected_assertions': [
                    ('result["strength"].rank', 5),
                    ('result["strength"].value', 10000),
                    ('result["speed"].rank', 12),
                    ('result["speed"].value', 8500)
                ]
            },
            {
                'section_name': 'honors',
                'method_name': 'fetch_data',
                'mock_response': {
                    'honors_awarded': [101, 102, 103],
                    'honors_time': [1635023000, 1635024000, 1635025000]
                },
                'expected_assertions': [
                    ('result["awarded"]', [101, 102, 103]),
                    ('result["times"]', [1635023000, 1635024000, 1635025000])
                ]
            },
            {
                'section_name': 'icons',
                'method_name': 'fetch_data',
                'mock_response': {
                    'icons': {
                        'status': 'active',
                        'badges': [1, 2, 3]
                    }
                },
                'expected_assertions': [
                    ('result["status"]', 'active'),
                    ('result["badges"]', [1, 2, 3])
                ]
            },
            {
                'section_name': 'jobpoints',
                'method_name': 'fetch_data',
                'mock_response': {
                    'jobpoints': {
                        'education': 5,
                        'medical': 3
                    }
                },
                'expected_assertions': [
                    ('result["education"]', 5),
                    ('result["medical"]', 3)
                ]
            },
            {
                'section_name': 'log',
                'method_name': 'fetch_data',
                'mock_response': {
                    'log': {
                        1: {
                            'timestamp': 1680000000,
                            'log': 'Example log entry 1'
                        },
                        2: {
                            'timestamp': 1680000100,
                            'log': 'Example log entry 2'
                        }
                    }
                },
                'expected_assertions': [
                    ('result[1]["timestamp"]', 1680000000),
                    ('result[1]["log"]', 'Example log entry 1'),
                    ('result[2]["timestamp"]', 1680000100),
                    ('result[2]["log"]', 'Example log entry 2')
                ]
            },
            {
                'section_name': 'lookup',
                'method_name': 'fetch_data',
                'mock_response': {
                    'selections': ['selection1', 'selection2', 'selection3']
                },
                'expected_assertions': [
                    ('result[0]', 'selection1'),
                    ('result[1]', 'selection2'),
                    ('result[2]', 'selection3')
                ]
            },
            {
                'section_name': 'medals',
                'method_name': 'fetch_data',
                'mock_response': {
                    'medals_awarded': [1, 2, 3],
                    'medals_time': [1680000000, 1680100000, 1680200000]
                },
                'expected_assertions': [
                    ('result["medals_awarded"][0]', 1),
                    ('result["medals_awarded"][1]', 2),
                    ('result["medals_awarded"][2]', 3),
                    ('result["medals_time"][0]', 1680000000),
                    ('result["medals_time"][1]', 1680100000),
                    ('result["medals_time"][2]', 1680200000)
                ]
            },
            {
                'section_name': 'merits',
                'method_name': 'fetch_data',
                'mock_response': {
                    'merits': {
                        'Addiction Mitigation': 1,
                        'Awareness': 3,
                        'Bank Interest': 2
                    }
                },
                'expected_assertions': [
                    ('result.addiction_mitigation', 1),
                    ('result.awareness', 3),
                    ('result.bank_interest', 2)
                ]
            },
            {
                'section_name': 'messages',
                'method_name': 'fetch_data',
                'mock_response': {
                    'messages': {
                        1: {
                            'name': 'User1',
                            'read': 0,
                            'seen': 1,
                            'timestamp': 1680000000,
                            'title': 'Test Message 1',
                            'type': 'normal'
                        },
                        2: {
                            'name': 'User2',
                            'read': 1,
                            'seen': 1,
                            'timestamp': 1680000100,
                            'title': 'Test Message 2',
                            'type': 'event'
                        }
                    }
                },
                'expected_assertions': [
                    ('result[1].name', 'User1'),
                    ('result[1].read', False),
                    ('result[1].seen', True),
                    ('result[1].timestamp', 1680000000),
                    ('result[1].title', 'Test Message 1'),
                    ('result[1].type', 'normal'),
                    ('result[2].name', 'User2'),
                    ('result[2].read', True),
                    ('result[2].seen', True),
                    ('result[2].timestamp', 1680000100),
                    ('result[2].title', 'Test Message 2'),
                    ('result[2].type', 'event')
                ]
            },
            {
                'section_name': 'missions',
                'method_name': 'fetch_data',
                'mock_response': {
                    'missions': {
                        'Duke': [
                            {'status': 'completed', 'title': 'Mission 1'},
                            {'status': 'notAccepted', 'title': 'Mission 2'}
                        ],
                        'Larry': [
                            {'status': 'inProgress', 'title': 'Mission 3'}
                        ]
                    }
                },
                'expected_assertions': [
                    ('result["Duke"][0].status', 'completed'),
                    ('result["Duke"][0].title', 'Mission 1'),
                    ('result["Duke"][1].status', 'notAccepted'),
                    ('result["Duke"][1].title', 'Mission 2'),
                    ('result["Larry"][0].status', 'inProgress'),
                    ('result["Larry"][0].title', 'Mission 3')
                ]
            },
            {
                'section_name': 'money',
                'method_name': 'fetch_data',
                'mock_response': {
                    'cayman_bank': 1000000,
                    'city_bank': {
                        'amount': 5000000,
                        'time_left': 3600
                    },
                    'company_funds': 500000,
                    'daily_networth': 10000000,
                    'money_onhand': 100000,
                    'points': 1000,
                    'vault_amount': 2000000
                },
                'expected_assertions': [
                    ('result.cayman_bank', 1000000),
                    ('result.city_bank.amount', 5000000),
                    ('result.city_bank.time_left', 3600),
                    ('result.company_funds', 500000),
                    ('result.daily_networth', 10000000),
                    ('result.money_onhand', 100000),
                    ('result.points', 1000),
                    ('result.vault_amount', 2000000)
                ]
            },
            {
                'section_name': 'networth',
                'method_name': 'fetch_data',
                'mock_response': {
                    'networth': {
                        'auctionhouse': 100000,
                        'bank': 5000000,
                        'bazaar': 200000,
                        'bookie': 50000,
                        'cayman': 1000000,
                        'company': 500000,
                        'displaycase': 300000,
                        'enlistedcars': 400000,
                        'itemmarket': 150000,
                        'items': 250000,
                        'loan': -100000,
                        'parsetime': 0.5,
                        'pending': 75000,
                        'piggybank': 25000,
                        'points': 1000,
                        'properties': 2000000,
                        'stockmarket': 1500000,
                        'total': 11450000,
                        'trade': 80000,
                        'unpaidfees': -20000,
                        'vault': 2000000,
                        'wallet': 100000
                    }
                },
                'expected_assertions': [
                    ('result.auctionhouse', 100000),
                    ('result.bank', 5000000),
                    ('result.bazaar', 200000),
                    ('result.bookie', 50000),
                    ('result.cayman', 1000000),
                    ('result.company', 500000),
                    ('result.displaycase', 300000),
                    ('result.enlistedcars', 400000),
                    ('result.itemmarket', 150000),
                    ('result.items', 250000),
                    ('result.loan', -100000),
                    ('result.parsetime', 0.5),
                    ('result.pending', 75000),
                    ('result.piggybank', 25000),
                    ('result.points', 1000),
                    ('result.properties', 2000000),
                    ('result.stockmarket', 1500000),
                    ('result.total', 11450000),
                    ('result.trade', 80000),
                    ('result.unpaidfees', -20000),
                    ('result.vault', 2000000),
                    ('result.wallet', 100000)
                ]
            },
            {
                'section_name': 'newevents',
                'method_name': 'fetch_data',
                'mock_response': {
                    'events': {
                        '1': {
                            'event': 'You were attacked by SomeUser',
                            'seen': 0,
                            'timestamp': 1624000000
                        },
                        '2': {
                            'event': 'You found $100 on the ground',
                            'seen': 0,
                            'timestamp': 1624000100
                        }
                    },
                    'player_id': 12345
                },
                'expected_assertions': [
                    ('result.player_id', 12345),
                    ('len(result.events)', 2),
                    ('result.events["1"].event', 'You were attacked by SomeUser'),
                    ('result.events["1"].seen', 0),
                    ('result.events["1"].timestamp', 1624000000),
                    ('result.events["2"].event', 'You found $100 on the ground'),
                    ('result.events["2"].seen', 0),
                    ('result.events["2"].timestamp', 1624000100)
                ]
            },
            {
                'section_name': 'newmessages',
                'method_name': 'fetch_data',
                'mock_response': {
                    'messages': {
                        '1': {
                            'ID': 101,
                            'name': 'Sender1',
                            'read': 0,
                            'seen': 0,
                            'timestamp': 1624000000,
                            'title': 'Message 1',
                            'type': 'Private'
                        },
                        '2': {
                            'ID': 102,
                            'name': 'Sender2',
                            'read': 0,
                            'seen': 0,
                            'timestamp': 1624000100,
                            'title': 'Message 2',
                            'type': 'Faction'
                        }
                    },
                    'player_id': 12345
                },
                'expected_assertions': [
                    ('result.player_id', 12345),
                    ('len(result.messages)', 2),
                    ('result.messages["1"].ID', 101),
                    ('result.messages["1"].name', 'Sender1'),
                    ('result.messages["1"].read', 0),
                    ('result.messages["1"].seen', 0),
                    ('result.messages["1"].timestamp', 1624000000),
                    ('result.messages["1"].title', 'Message 1'),
                    ('result.messages["1"].type', 'Private'),
                    ('result.messages["2"].ID', 102),
                    ('result.messages["2"].name', 'Sender2'),
                    ('result.messages["2"].type', 'Faction')
                ]
            },
            {
                'section_name': 'notifications',
                'method_name': 'fetch_data',
                'mock_response': {
                    'awards': 2,
                    'competition': 1,
                    'events': 5,
                    'messages': 3
                },
                'expected_assertions': [
                    ('result.awards', 2),
                    ('result.competition', 1),
                    ('result.events', 5),
                    ('result.messages', 3)
                ]
            },
            {
                'section_name': 'perks',
                'method_name': 'fetch_data',
                'mock_response': {
                    'book_perks': ['Speed Reading I', 'Speed Reading II'],
                    'education_perks': ['Bachelor of Science'],
                    'enhancer_perks': ['Energy Drink'],
                    'faction_perks': ['Armor Bonus', 'Weapon Bonus'],
                    'job_perks': ['Employee Discount'],
                    'merit_perks': ['ATM Interest'],
                    'property_perks': ['Rent Income'],
                    'stock_perks': ['Dividend Rate']
                },
                'expected_assertions': [
                    ('result.book_perks', ['Speed Reading I', 'Speed Reading II']),
                    ('result.education_perks', ['Bachelor of Science']),
                    ('result.enhancer_perks', ['Energy Drink']),
                    ('result.faction_perks', ['Armor Bonus', 'Weapon Bonus']),
                    ('result.job_perks', ['Employee Discount']),
                    ('result.merit_perks', ['ATM Interest']),
                    ('result.property_perks', ['Rent Income']),
                    ('result.stock_perks', ['Dividend Rate'])
                ]
            },
            {
                'section_name': 'personalstats',  # Name of the section
                'method_name': 'fetch_data',      # Method to fetch data for the section
                'mock_response': {                 # Simulated API response data
                    'personalstats': {
                        'activestreak': 10,
                        'alcoholused': 5,
                        'argtravel': 7,
                        'arrestsmade': 3,
                        'attackcriticalhits': 12,
                        'attackdamage': 3500,
                        'attackhits': 200,
                        'attackmisses': 50,
                        'attacksassisted': 15,
                        'attacksdraw': 1,
                        'attackslost': 8,
                        'attacksstealthed': 4,
                        'attackswon': 180,
                        'attackswonabroad': 10,
                        'auctionsells': 25,
                        'auctionswon': 30,
                        'awards': 100,
                        'axehits': 40,
                        'bazaarcustomers': 20,
                        'bazaarprofit': 1000000,
                        'bazaarsales': 50,
                        'bestactivestreak': 12,
                        'bestdamage': 4500,
                        'bestkillstreak': 6,
                        'bloodwithdrawn': 25,
                        'booksread': 5,
                        'boostersused': 3,
                        'bountiescollected': 10,
                        'bountiesplaced': 5,
                        'bountiesreceived': 2,
                        'candyused': 10,
                        'cantaken': 1,
                        'cantravel': 0,
                        'caytravel': 0,
                        'chahits': 20,
                        'chitravel': 0,
                        'cityfinds': 100,
                        'cityitemsbought': 50,
                        'classifiedadsplaced': 5,
                        'companymailssent': 10,
                        'consumablesused': 30,
                        'contractscompleted': 7,
                        'counterfeiting': 1000,
                        'criminaloffenses': 200,
                        'cybercrime': 150,
                        'daysbeendonator': 365,
                        'defendslost': 3,
                        'defendslostabroad': 2,
                        'defendsstalemated': 1,
                        'defendswon': 50,
                        'defense': 1000,
                        'dexterity': 900,
                        'drugsused': 20,
                        'dubtravel': 3,
                        'dukecontractscompleted': 1,
                        'dumpfinds': 15,
                        'dumpsearches': 25,
                        'eastereggs': 10,
                        'eastereggsused': 5,
                        'elo': 1200,
                        'endurance': 800,
                        'energydrinkused': 10,
                        'extortion': 2000,
                        'exttaken': 5,
                        'factionmailssent': 20,
                        'failedbusts': 5,
                        'fraud': 500,
                        'friendmailssent': 15,
                        'grehits': 10,
                        'h2hhits': 25,
                        'hawtravel': 2,
                        'heahits': 30,
                        'highestbeaten': 100,
                        'hollowammoused': 50,
                        'hospital': 20,
                        'illegalproduction': 500,
                        'illicitservices': 300,
                        'incendiaryammoused': 40,
                        'intelligence': 700,
                        'investedprofit': 50000,
                        'itemsbought': 100,
                        'itemsboughtabroad': 20,
                        'itemsdumped': 30,
                        'itemslooted': 75,
                        'itemssent': 40,
                        'jailed': 10,
                        'japtravel': 1,
                        'jobpointsused': 25,
                        'kettaken': 2,
                        'killstreak': 5,
                        'largestmug': 10000,
                        'lontravel': 3,
                        'lsdtaken': 1,
                        'machits': 25,
                        'mailssent': 50,
                        'manuallabor': 2000,
                        'medicalitemsused': 15,
                        'meritsbought': 12,
                        'mextravel': 2,
                        'missioncreditsearned': 200,
                        'missionscompleted': 150,
                        'moneyinvested': 100000,
                        'moneymugged': 5000,
                        'nerverefills': 10,
                        'networth': 2000000,
                        'networthauctionhouse': 100000,
                        'networthbank': 50000,
                        'networthbazaar': 300000,
                        'networthbookie': 25000,
                        'networthcayman': 100000,
                        'networthcompany': 150000,
                        'networthdisplaycase': 50000,
                        'networthenlistedcars': 20000,
                        'networthitemmarket': 30000,
                        'networthitems': 100000,
                        'networthloan': 5000,
                        'networthpending': 2000,
                        'networthpiggybank': 1000,
                        'networthpoints': 20000,
                        'networthproperties': 500000,
                        'networthstockmarket': 100000,
                        'networthunpaidfees': 1000,
                        'networthvault': 500000,
                        'networthwallet': 10000,
                        'onehitkills': 15,
                        'opitaken': 3,
                        'organisedcrimes': 25,
                        'overdosed': 1,
                        'pcptaken': 2,
                        'peoplebought': 10,
                        'peopleboughtspent': 5000,
                        'peoplebusted': 7,
                        'personalsplaced': 2,
                        'piehits': 20,
                        'piercingammoused': 10,
                        'pishits': 15,
                        'pointsbought': 1000,
                        'pointssold': 500,
                        'racesentered': 50,
                        'raceswon': 10,
                        'racingpointsearned': 100,
                        'racingskill': 75,
                        'raidhits': 30,
                        'rankedwarhits': 20,
                        'rankedwarringwins': 10,
                        'receivedbountyvalue': 3000,
                        'refills': 25,
                        'rehabcost': 15000,
                        'rehabs': 3,
                        'respectforfaction': 50000,
                        'retals': 10,
                        'revives': 20,
                        'reviveskill': 50,
                        'revivesreceived': 5,
                        'rifhits': 30,
                        'roundsfired': 1000,
                        'shohits': 20,
                        'shrtaken': 1,
                        'slahits': 25,
                        'smghits': 40,
                        'soutravel': 3,
                        'specialammoused': 10,
                        'speed': 1200,
                        'spetaken': 1,
                        'spousemailssent': 5,
                        'statenhancersused': 10,
                        'stockfees': 2000,
                        'stocklosses': 1500,
                        'stocknetprofits': 5000,
                        'stockpayouts': 10000,
                        'stockprofits': 2500,
                        'strength': 1500,
                        'switravel': 1,
                        'territoryclears': 10,
                        'territoryjoins': 20,
                        'territorytime': 500,
                        'theft': 300,
                        'theyrunaway': 5,
                        'tokenrefills': 3,
                        'totalbountyreward': 10000,
                        'totalbountyspent': 5000,
                        'totalstats': 50000,
                        'totalworkingstats': 25000,
                        'tracerammoused': 5,
                        'trades': 100,
                        'trainsreceived': 15,
                        'traveltime': 100,
                        'traveltimes': 50,
                        'unarmoredwon': 20,
                        'useractivity': 95,
                        'victaken': 2,
                        'virusescoded': 5,
                        'weaponsbought': 50,
                        'xantaken': 200,
                        'yourunaway': 3,
                    }
                },
                'expected_assertions': [
                ('result.activestreak', 10),
                ('result.alcoholused', 5),
                ('result.argtravel', 7),
                ('result.arrestsmade', 3),
                ('result.attackcriticalhits', 12),
                ('result.attackdamage', 3500),
                ('result.attackhits', 200),
                ('result.attackmisses', 50),
                ('result.attacksassisted', 15),
                ('result.attacksdraw', 1),
                ('result.attackslost', 8),
                ('result.attacksstealthed', 4),
                ('result.attackswon', 180),
                ('result.attackswonabroad', 10),
                ('result.auctionsells', 25),
                ('result.auctionswon', 30),
                ('result.awards', 100),
                ('result.axehits', 40),
                ('result.bazaarcustomers', 20),
                ('result.bazaarprofit', 1000000),
                ('result.bazaarsales', 50),
                ('result.bestactivestreak', 12),
                ('result.bestdamage', 4500),
                ('result.bestkillstreak', 6),
                ('result.bloodwithdrawn', 25),
                ('result.booksread', 5),
                ('result.boostersused', 3),
                ('result.bountiescollected', 10),
                ('result.bountiesplaced', 5),
                ('result.bountiesreceived', 2),
                ('result.candyused', 10),
                ('result.cantaken', 1),
                ('result.cantravel', 0),
                ('result.caytravel', 0),
                ('result.chahits', 20),
                ('result.chitravel', 0),
                ('result.cityfinds', 100),
                ('result.cityitemsbought', 50),
                ('result.classifiedadsplaced', 5),
                ('result.companymailssent', 10),
                ('result.consumablesused', 30),
                ('result.contractscompleted', 7),
                ('result.counterfeiting', 1000),
                ('result.criminaloffenses', 200),
                ('result.cybercrime', 150),
                ('result.daysbeendonator', 365),
                ('result.defendslost', 3),
                ('result.defendslostabroad', 2),
                ('result.defendsstalemated', 1),
                ('result.defendswon', 50),
                ('result.defense', 1000),
                ('result.dexterity', 900),
                ('result.drugsused', 20),
                ('result.dubtravel', 3),
                ('result.dukecontractscompleted', 1),
                ('result.dumpfinds', 15),
                ('result.dumpsearches', 25),
                ('result.eastereggs', 10),
                ('result.eastereggsused', 5),
                ('result.elo', 1200),
                ('result.endurance', 800),
                ('result.energydrinkused', 10),
                ('result.extortion', 2000),
                ('result.exttaken', 5),
                ('result.factionmailssent', 20),
                ('result.failedbusts', 5),
                ('result.fraud', 500),
                ('result.friendmailssent', 15),
                ('result.grehits', 10),
                ('result.h2hhits', 25),
                ('result.hawtravel', 2),
                ('result.heahits', 30),
                ('result.highestbeaten', 100),
                ('result.hollowammoused', 50),
                ('result.hospital', 20),
                ('result.illegalproduction', 500),
                ('result.illicitservices', 300),
                ('result.incendiaryammoused', 40),
                ('result.intelligence', 700),
                ('result.investedprofit', 50000),
                ('result.itemsbought', 100),
                ('result.itemsboughtabroad', 20),
                ('result.itemsdumped', 30),
                ('result.itemslooted', 75),
                ('result.itemssent', 40),
                ('result.jailed', 10),
                ('result.japtravel', 1),
                ('result.jobpointsused', 25),
                ('result.kettaken', 2),
                ('result.killstreak', 5),
                ('result.largestmug', 10000),
                ('result.lontravel', 3),
                ('result.lsdtaken', 1),
                ('result.machits', 25),
                ('result.mailssent', 50),
                ('result.manuallabor', 2000),
                ('result.medicalitemsused', 15),
                ('result.meritsbought', 12),
                ('result.mextravel', 2),
                ('result.missioncreditsearned', 200),
                ('result.missionscompleted', 150),
                ('result.moneyinvested', 100000),
                ('result.moneymugged', 5000),
                ('result.nerverefills', 10),
                ('result.networth', 2000000),
                ('result.networthauctionhouse', 100000),
                ('result.networthbank', 50000),
                ('result.networthbazaar', 300000),
                ('result.networthbookie', 25000),
                ('result.networthcayman', 100000),
                ('result.networthcompany', 150000),
                ('result.networthdisplaycase', 50000),
                ('result.networthenlistedcars', 20000),
                ('result.networthitemmarket', 30000),
                ('result.networthitems', 100000),
                ('result.networthloan', 5000),
                ('result.networthpending', 2000),
                ('result.networthpiggybank', 1000),
                ('result.networthpoints', 20000),
                ('result.networthproperties', 500000),
                ('result.networthstockmarket', 100000),
                ('result.networthunpaidfees', 1000),
                ('result.networthvault', 500000),
                ('result.networthwallet', 10000),
                ('result.onehitkills', 15),
                ('result.opitaken', 3),
                ('result.organisedcrimes', 25),
                ('result.overdosed', 1),
                ('result.pcptaken', 2),
                ('result.peoplebought', 10),
                ('result.peopleboughtspent', 5000),
                ('result.peoplebusted', 7),
                ('result.personalsplaced', 2),
                ('result.piehits', 20),
                ('result.piercingammoused', 10),
                ('result.pishits', 15),
                ('result.pointsbought', 1000),
                ('result.pointssold', 500),
                ('result.racesentered', 50),
                ('result.raceswon', 10),
                ('result.racingpointsearned', 100),
                ('result.racingskill', 75),
                ('result.raidhits', 30),
                ('result.rankedwarhits', 20),
                ('result.rankedwarringwins', 10),
                ('result.receivedbountyvalue', 3000),
                ('result.refills', 25),
                ('result.rehabcost', 15000),
                ('result.rehabs', 3),
                ('result.respectforfaction', 50000),
                ('result.retals', 10),
                ('result.revives', 20),
                ('result.reviveskill', 50),
                ('result.revivesreceived', 5),
                ('result.rifhits', 30),
                ('result.roundsfired', 1000),
                ('result.shohits', 20),
                ('result.shrtaken', 1),
                ('result.slahits', 25),
                ('result.smghits', 40),
                ('result.soutravel', 3),
                ('result.specialammoused', 10),
                ('result.speed', 1200),
                ('result.spetaken', 1),
                ('result.spousemailssent', 5),
                ('result.statenhancersused', 10),
                ('result.stockfees', 2000),
                ('result.stocklosses', 1500),
                ('result.stocknetprofits', 5000),
                ('result.stockpayouts', 10000),
                ('result.stockprofits', 2500),
                ('result.strength', 1500),
                ('result.switravel', 1),
                ('result.territoryclears', 10),
                ('result.territoryjoins', 20),
                ('result.territorytime', 500),
                ('result.theft', 300),
                ('result.theyrunaway', 5),
                ('result.tokenrefills', 3),
                ('result.totalbountyreward', 10000),
                ('result.totalbountyspent', 5000),
                ('result.totalstats', 50000),
                ('result.totalworkingstats', 25000),
                ('result.tracerammoused', 5),
                ('result.trades', 100),
                ('result.trainsreceived', 15),
                ('result.traveltime', 100),
                ('result.traveltimes', 50),
                ('result.unarmoredwon', 20),
                ('result.useractivity', 95),
                ('result.victaken', 2),
                ('result.virusescoded', 5),
                ('result.weaponsbought', 50),
                ('result.xantaken', 200),
                ('result.yourunaway', 3),
                ],
            },
            {
                'section_name': 'profile',  # Name of the section (e.g., 'profile')
                'method_name': 'fetch_data',  # Method to fetch profile data
                'mock_response': {
                    'age': 500,
                    'awards': 10,
                    'basicicons': {},
                    'competition': {
                        'attacks': 20,
                        'image': '',
                        'name': 'Competition Name',
                        'position': '1st',
                        'score': 100,
                        'status': 'Active',
                        'team': 'Team A',
                        'text': '',
                        'total': 200,
                        'treats_collected_total': 500,
                        'votes': 20
                    },
                    'donator': 1,
                    'enemies': 5,
                    'faction': {
                        'days_in_faction': 100,
                        'faction_id': 1234,
                        'faction_name': 'FactionName',
                        'faction_tag': '[TAG]',
                        'position': 'Member'
                    },
                    'forum_posts': 150,
                    'friends': 50,
                    'gender': 'Male',
                    'honor': 1000,
                    'job': {
                        'company_id': 5678,
                        'company_name': 'CompanyName',
                        'company_type': 3,
                        'job': 'Manager',
                        'position': 'Top'
                    },
                    'karma': 75,
                    'last_action': {
                        'relative': '5 minutes ago',
                        'status': 'Online',
                        'timestamp': 1696001234
                    },
                    'level': 50,
                    'life': {
                        'current': 1000,
                        'fulltime': 60,
                        'increment': 5,
                        'interval': 10,
                        'maximum': 1000,
                        'ticktime': 1696001300
                    },
                    'married': {
                        'duration': 300,
                        'spouse_id': 98765,
                        'spouse_name': 'SpouseName'
                    },
                    'name': 'TestUser',
                    'player_id': 54321,
                    'profile_image': 'https://example.com/image.jpg',
                    'property': 'Mansion',
                    'property_id': 78910,
                    'rank': 'General',
                    'revivable': 1,
                    'role': 'Leader',
                    'signup': '2020-01-01',
                    'states': {
                        'hospital_timestamp': 1696001400,
                        'jail_timestamp': 1696001450
                    },
                    'status': {
                        'color': 'green',
                        'description': 'Healthy',
                        'details': 'No issues',
                        'state': 'Okay',
                        'until': 0
                    }
                },  # Simulated API response data for testing purposes
                'expected_assertions': [
                    ('result.age', 500),
                    ('result.name', 'TestUser'),
                    ('result.level', 50),
                    ('result.faction.faction_name', 'FactionName'),
                    ('result.life.current', 1000),
                    ('result.status.state', 'Okay'),
                    ('result.married.spouse_name', 'SpouseName')
                ]
            },
            {
                'section_name': 'properties',  # Name of the section
                'method_name': 'fetch_data',   # Method to fetch data for the section
                'mock_response': {
                    "properties": {
                        "1": {
                            "owner_id": 3154835,
                            "property_type": "House",
                            "property": "Cozy Cottage",
                            "status": "Happy",
                            "happy": 100,
                            "upkeep": 50,
                            "staff_cost": 20,
                            "cost": 150000,
                            "marketprice": 200000,
                            "modifications": {
                                "interior": 1,
                                "hot_tub": 0,
                                "sauna": 1,
                                "pool": 0,
                                "open_bar": 1,
                                "shooting_range": 0,
                                "vault": 1,
                                "medical_facility": 0,
                                "airstrip": 0,
                                "yacht": 0
                            },
                            "staff": {
                                "maid": 1,
                                "guard": 0,
                                "pilot": 0,
                                "butler": 1,
                                "doctor": 0
                            },
                            "rented": {
                                "cost_per_day": 100,
                                "days_left": 30,
                                "total_cost": 3000,
                                "user_id": 1234567
                            }
                        }
                    }
                },  # Simulated API response data for testing purposes
                'expected_assertions': [
                    ('result.properties[0].property_data.property_name', 'Cozy Cottage'),
                    ('result.properties[0].property_data.owner_id', 3154835),
                    ('result.properties[0].property_data.happy', 100),
                    ('result.properties[0].property_data.upkeep', 50),
                    ('result.properties[0].property_data.staff_cost', 20),
                    ('result.properties[0].property_data.cost', 150000),
                    ('result.properties[0].property_data.marketprice', 200000),
                    ('result.properties[0].property_data.rented.user_id', 1234567)
                ]
            },
            {
                'section_name': 'public_status',  # Name of the section
                'method_name': 'fetch_data',   # Method to fetch data for the section
                'mock_response': {
                    "baned": False,
                    "playername": "CoolPlayer",
                    "status": "Online",
                    "userID": 3154835
                },  # Simulated API response data for testing purposes
                'expected_assertions': [
                    ('result.playername', 'CoolPlayer'),
                    ('result.status', 'Online'),
                    ('result.user_id', 3154835),
                    ('result.baned', False)
                ]
            },
            {
                'section_name': 'refills',  # Name of the section
                'method_name': 'fetch_data',   # Method to fetch data for the section
                'mock_response': {
                    "refills": {
                        "energy_refill_used": True,
                        "nerve_refill_used": False,
                        "special_refills_available": 3,
                        "token_refill_used": True
                    }
                },  # Simulated API response data for testing purposes
                'expected_assertions': [
                    ('result.energy_refill_used', True),
                    ('result.nerve_refill_used', False),
                    ('result.special_refills_available', 3),
                    ('result.token_refill_used', True)
                ]
            },
            # TODO: Reports not functioning correctly
            # {
            #     'section_name': 'reports',  # Name of the section
            #     'method_name': 'fetch_data',   # Method to fetch data for the section
            #     'mock_response': {
            #         "reports": [
            #             {
            #                 "id": "12345",
            #                 "target": 3154835,
            #                 "timestamp": 1691650445,
            #                 "type": "battle",
            #                 "user_id": 1234567,
            #                 "report": {
            #                     "bounties": [],
            #                     "company_history": [],
            #                     "defense": 50,
            #                     "dexterity": 30,
            #                     "enemylist": [
            #                         {"name": "Enemy One", "user_id": 111},
            #                         {"name": "Enemy Two", "user_id": 222}
            #                     ],
            #                     "faction_history": [],
            #                     "friendlist": [
            #                         {"name": "Friend One", "user_id": 333}
            #                     ],
            #                     "invested_amount": 1000,
            #                     "invested_completion": "50%",
            #                     "money": 500,
            #                     "otherlist": [],
            #                     "speed": 20,
            #                     "strength": 60,
            #                     "toplist": [],
            #                     "total_battlestats": 100,
            #                     "truelevel": 5
            #                 }
            #             },
            #             {
            #                 "id": "12346",
            #                 "target": 3154835,
            #                 "timestamp": 1691650444,
            #                 "type": "battle",
            #                 "user_id": 1234567,
            #                 "report": {
            #                     "bounties": [],
            #                     "company_history": [],
            #                     "defense": 50,
            #                     "dexterity": 30,
            #                     "enemylist": [
            #                         {"name": "Enemy One", "user_id": 111},
            #                         {"name": "Enemy Two", "user_id": 222}
            #                     ],
            #                     "faction_history": [],
            #                     "friendlist": [
            #                         {"name": "Friend One", "user_id": 333}
            #                     ],
            #                     "invested_amount": 1000,
            #                     "invested_completion": "50%",
            #                     "money": 500,
            #                     "otherlist": [],
            #                     "speed": 20,
            #                     "strength": 60,
            #                     "toplist": [],
            #                     "total_battlestats": 100,
            #                     "truelevel": 5
            #                 }
            #             }
            #             # You can add more mock reports as needed
            #         ]
            #     },  # Simulated API response data for testing purposes
            #     'expected_assertions': [
            #         ('result[0].id', '12345'),
            #         ('result[0].target', 3154835),
            #         ('result[0].timestamp', 1691650445),
            #         ('result[0].type', 'battle'),
            #         ('result[0].user_id', 1234567),
            #         ('result[0].report.defense', 50),
            #         ('result[0].report.dexterity', 30),
            #         ('result[0].report.invested_amount', 1000),
            #         ('result[0].report.money', 500),
            #         ('result[0].report.enemylist[0].name', 'Enemy One'),
            #         ('result[0].report.friendlist[0].name', 'Friend One')
            #     ]
            # }
            {
                'section_name': 'revives',  # Name of the section
                'method_name': 'fetch_data',  # Method to fetch data for the section
                'mock_response': {
                    "revives": [
                        {
                            "timestamp": 1691650445,
                            "reviver_id": 123456,
                            "reviver_name": "Reviver One",
                            "reviver_faction": 1,
                            "reviver_factionname": "Faction A",
                            "target_id": 654321,
                            "target_name": "Target User",
                            "target_faction": 2,
                            "target_factionname": "Faction B",
                            "target_hospital_reason": "Battle Injury",
                            "target_last_action": {
                                "status": "Active",
                                "timestamp": 1691650300
                            },
                            "chance": 75.0,
                            "result": "Success"
                        }
                    ]
                },  # Simulated API response data for testing purposes
                'expected_assertions': [
                    ('result[0].timestamp', 1691650445),
                    ('result[0].reviver_id', 123456),
                    ('result[0].reviver_name', 'Reviver One'),
                    ('result[0].target_id', 654321),
                    ('result[0].target_name', 'Target User'),
                    ('result[0].result', 'Success'),
                    ('result[0].target_last_action.status', 'Active'),
                    ('result[0].target_last_action.timestamp', 1691650300),
                    ('result[0].chance', 75.0)
                ]
            },
            {
                'section_name': 'revives_full',  # Name of the section
                'method_name': 'fetch_data',  # Method to fetch data for the section
                'mock_response': {
                    "revives": [
                        {
                            "timestamp": 1691650445,
                            "reviver_id": 123456,
                            "reviver_faction": 1,
                            "target_id": 654321,
                            "target_faction": 2,
                            "target_hospital_reason": "Battle Injury",
                            "target_last_action": {
                                "status": "Active",
                                "timestamp": 1691650300
                            },
                            "chance": 75.0,
                            "result": "Success"
                        }
                        # You can add more mock revives as needed
                    ]
                },  # Simulated API response data for testing purposes
                'expected_assertions': [
                    ('result[0].timestamp', 1691650445),
                    ('result[0].reviver_id', 123456),
                    ('result[0].target_id', 654321),
                    ('result[0].target_hospital_reason', 'Battle Injury'),
                    ('result[0].target_last_action.status', 'Active'),
                    ('result[0].target_last_action.timestamp', 1691650300),
                    ('result[0].chance', 75.0),
                    ('result[0].result', 'Success')
                ]
            },
            {
                'section_name': 'skills',  # Name of the section
                'method_name': 'fetch_data',  # Method to fetch data for the section
                'mock_response': {
                    "player_id": 3154835,
                    "bootlegging": "1",
                    "burglary": "2",
                    "card_skimming": "3",
                    "cracking": "4",
                    "disposal": "5",
                    "forgery": "6",
                    "graffiti": "7",
                    "hunting": "8",
                    "hustling": "9",
                    "pickpocketing": "10",
                    "racing": "11",
                    "reviving": "12",
                    "search_for_cash": "13",
                    "shoplifting": "14"
                },  # Simulated API response data for testing purposes
                'expected_assertions': [
                    ('result.player_id', 3154835),
                    ('result.bootlegging', "1"),
                    ('result.burglary', "2"),
                    ('result.card_skimming', "3"),
                    ('result.cracking', "4"),
                    ('result.disposal', "5"),
                    ('result.forgery', "6"),
                    ('result.graffiti', "7"),
                    ('result.hunting', "8"),
                    ('result.hustling', "9"),
                    ('result.pickpocketing', "10"),
                    ('result.racing', "11"),
                    ('result.reviving', "12"),
                    ('result.search_for_cash', "13"),
                    ('result.shoplifting', "14")
                ]
            },
            # TODO: Stocks not functioning correctly
            #{
        #     'section_name': 'stocks',  # Name of the section
        #     'method_name': 'fetch_data',  # Method to fetch data for the section
        #     'mock_response': {
        #         "stocks": {
        #             "1": {
        #                 "benefit": {"name": "Stock Benefit", "active": True},
        #                 "dividend": {"amount": 5000, "last_payment": 1632968400},
        #                 "total_shares": 100,
        #                 "transactions": {"buy": 50, "sell": 20}
        #             },
        #             "2": {
        #                 "benefit": {"name": "Another Benefit", "active": False},
        #                 "dividend": {"amount": 3000, "last_payment": 1632968500},
        #                 "total_shares": 200,
        #                 "transactions": {"buy": 100, "sell": 30}
        #             }
        #         }
        #     },  # Simulated API response data for testing purposes
        #     'expected_assertions': [
        #         ('result.stocks[0].stock_id', "1"),
        #         ('result.stocks[0].benefit.name', "Stock Benefit"),
        #         ('result.stocks[0].benefit.active', True),
        #         ('result.stocks[0].dividend.amount', 5000),
        #         ('result.stocks[0].dividend.last_payment', 1632968400),
        #         ('result.stocks[0].total_shares', 100),
        #         ('result.stocks[0].transactions.buy', 50),
        #         ('result.stocks[0].transactions.sell', 20),
                
        #         ('result.stocks[1].stock_id', "2"),
        #         ('result.stocks[1].benefit.name', "Another Benefit"),
        #         ('result.stocks[1].benefit.active', False),
        #         ('result.stocks[1].dividend.amount', 3000),
        #         ('result.stocks[1].dividend.last_payment', 1632968500),
        #         ('result.stocks[1].total_shares', 200),
        #         ('result.stocks[1].transactions.buy', 100),
        #         ('result.stocks[1].transactions.sell', 30)
        #     ]
        # }
            {
                'section_name': 'timestamp',  # Name of the section
                'method_name': 'fetch_data',  # Method to fetch data for the section
                'mock_response': {
                    "timestamp": 1632968400  # Simulated current timestamp (epoch in seconds)
                },  # Simulated API response data for testing purposes
                'expected_assertions': [
                    ('result', 1632968400),  # Assertion to check if the timestamp matches the expected value
                ]
            },
            {
                'section_name': 'travel',  # Name of the section being tested
                'method_name': 'fetch_data',  # Method to fetch travel data
                'mock_response': {
                    "travel": {
                        "departed": 1632968400,  # Example epoch timestamp of departure
                        "destination": "Cayman Islands",  # Example destination
                        "method": "Private Jet",  # Example method of travel
                        "time_left": 3600,  # Time left in seconds (e.g., 1 hour)
                        "timestamp": 1632972000  # Example epoch timestamp
                    }
                },  # Simulated API response data for testing purposes
                'expected_assertions': [
                    ('result.departed', 1632968400),
                    ('result.destination', "Cayman Islands"),
                    ('result.method', "Private Jet"),
                    ('result.time_left', 3600),
                    ('result.timestamp', 1632972000)
                ]
            },
            {
                'section_name': 'weapon_exp',  # Name of the section being tested
                'method_name': 'fetch_data',  # Method to fetch weapon experience data
                'mock_response': {
                    "weaponexp": [
                        {
                            "itemID": 1234,  # Example weapon item ID
                            "exp": 567,  # Example weapon experience points
                            "name": "Desert Eagle"  # Example weapon name
                        },
                        {
                            "itemID": 4321,
                            "exp": 890,
                            "name": "AK-47"
                        }
                    ]
                },  # Simulated API response data for testing purposes
                'expected_assertions': [
                    ('result.weapon_experiences[0].itemID', 1234),
                    ('result.weapon_experiences[0].exp', 567),
                    ('result.weapon_experiences[0].name', "Desert Eagle"),
                    ('result.weapon_experiences[1].itemID', 4321),
                    ('result.weapon_experiences[1].exp', 890),
                    ('result.weapon_experiences[1].name', "AK-47")
                ]
            },  
            {
                'section_name': 'work_stats',  # Name of the section (e.g., 'workstats')
                'method_name': 'fetch_data',  # Method to fetch work stats
                'mock_response': {
                    'endurance': 85,  # Example endurance value
                    'intelligence': 90,  # Example intelligence value
                    'manual_labor': 70  # Example manual labor value
                },  # Simulated API response data for testing purposes
                'expected_assertions': [
                    ('result.endurance', 85),
                    ('result.intelligence', 90),
                    ('result.manual_labor', 70)
                ]
            }
        ]
        
        

        for index, test_case in enumerate(test_cases):
            with self.subTest(section=test_case['section_name']):
                logger.info(f"Starting test case {index + 1}/{len(test_cases)}: Section '{test_case['section_name']}', Method '{test_case['method_name']}'")
                
                with patch.object(self.api, 'make_request', return_value=test_case['mock_response']):
                    # Get the section instance and method
                    section = getattr(self.user, test_case['section_name'])
                    logger.debug(f"Retrieved section: {section}")
                    
                    method = getattr(section, test_case['method_name'])
                    logger.debug(f"Retrieved method: {method}")

                    # Call the method and get the result
                    logger.info(f"Calling method '{test_case['method_name']}' on section '{test_case['section_name']}'")
                    result = method()
                    logger.info(f"Result obtained from '{test_case['method_name']}': {result}")

                    # Verify all expected assertions
                    for assertion, expected_value in test_case['expected_assertions']:
                        logger.debug(f"Evaluating assertion: {assertion}")
                        actual_value = eval(assertion)

                        # Log detailed information about the assertion
                        logger.warning(f"Assertion: '{assertion}' | Expected Value: '{expected_value}' | Actual Value: '{actual_value}'")

                        self.assertEqual(actual_value, expected_value, 
                            f"{test_case['section_name']}: Expected '{assertion}' to be '{expected_value}', but got '{actual_value}'")
                    
                    # Verify that the API was called exactly once
                    self.api.make_request.assert_called_once()
                    logger.info(f"API call for section '{test_case['section_name']}' and method '{test_case['method_name']}' was called exactly once.")
                    logger.info(f"Completed test case {index + 1}/{len(test_cases)}: '{test_case['section_name']}'")

    def test_fetch_with_no_data(self):
        """Test fetching when API returns no data for all sections."""
        # Define the sections and their expected behavior when no data is returned
        sections_to_test = [
            ('ammo', 'fetch_data', []),
            ('attacks', 'fetch_data', []),
            ('attacks_full', 'fetch_data', []),
            ('bars', 'fetch_data', None),
            ('basic', 'fetch_data', None),
            ('battle_stats', 'fetch_data', None),
            ('bazaar', 'fetch_data', []),
            ('cooldowns', 'fetch_data', None),
            ('crimes', 'fetch_data', None),
            ('criminal_record', 'fetch_data', None),
            ('discord', 'fetch_data', None),
            ('display_items', 'fetch_data', []),
            ('education', 'fetch_data', None),
            ('equipment', 'fetch_data', []),  # Added Equipment section
            ('events', 'fetch_data', []),          # Added Events section
            ('gym', 'fetch_data', None),              # Added Gym section
            ('hof', 'fetch_data', {}),              # Added HallOfFame section
            ('honors', 'fetch_data', {}),        # Added Honors section
            ('icons', 'fetch_data', {}),          # Added Icons section
            ('jobpoints', 'fetch_data', {}),  # Added JobPoints section
            ('log', 'fetch_data', {}),              # Added Log section
            ('medals', 'fetch_data', {}),        # Added Medals section
            ('merits', 'fetch_data', None),        # Added Merits section
            ('messages', 'fetch_data', None),    # Added Messages section
            ('missions', 'fetch_data', None),    # Added Missions section
            ('money', 'fetch_data', None),          # Added Money section
            ('networth', 'fetch_data', None),    # Added Networth section
            ('newevents', 'fetch_data', None),     # Added NewEvents section
            ('newmessages', 'fetch_data', None),  # Added NewMessages section
            ('notifications', 'fetch_data', None),  # Added Notifications section
            ('perks', 'fetch_data', None),          # Added Perks section
            ('personalstats', 'fetch_data', None),  # Added PersonalStats section
            ('profile', 'fetch_data', None),      # Added Profile section
            ('properties', 'fetch_data', None), # Added Properties section
            ('public_status', 'fetch_data', None), # Added PublicStatus section
            ('refills', 'fetch_data', None),      # Added Refills section
            ('reports', 'fetch_data', []),      # Added Reports section
            ('revives', 'fetch_data', []),      # Added Revives section
            ('revives_full', 'fetch_data', []), # Added RevivesFull section
            ('skills', 'fetch_data', None),        # Added Skills section
            ('stocks', 'fetch_data', None),        # Added Stocks section
            ('timestamp', 'fetch_data', None),  # Added Timestamp section
            ('travel', 'fetch_data', None),        # Added Travel section
            ('weapon_exp', 'fetch_data', None), # Added WeaponExp section
            ('work_stats', 'fetch_data', None), # Added WorkStats section
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
    unittest.main()