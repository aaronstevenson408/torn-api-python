# sections.py

import logging
from typing import Dict, Any, Optional
from main_api import TornAPI
from env_loader import load_environment_variables
from logger import setup_logger, close_logger

env = load_environment_variables()
if env is None:
    raise ValueError("Failed to load environment variables.")
logger, file_handler = setup_logger('sections', env['DEBUG_LEVEL'])
class User:
    def __init__(self, api: TornAPI, user_id: Optional[int] = None):
        self.api = api
        self.user_id = user_id
        self.ammo = self.Ammo(self.api, self.user_id)
        self.basic = self.Basic(self.api, self.user_id)
        self.attacks = self.Attacks(self.api, self.user_id)
        self.attacksfull = self.AttacksFull(self.api, self.user_id)
        self.bars = self.Bars(self.api, self.user_id)
        self.battlestats = self.BattleStats(self.api, self.user_id)
        self.bazaar = self.Bazaar(self.api, self.user_id)
        self.cooldowns = self.Cooldowns(self.api, self.user_id)
        self.crimes = self.Crimes(self.api, self.user_id)
        self.criminal_record = self.CriminalRecord(self.api, self.user_id)
        self.discord = self.Discord(self.api, self.user_id)
        self.display_items = self.DisplayItems(self.api, self.user_id)
        self.education = self.Education(self.api, self.user_id)  # Added Education class
        self.equipment = self.Equipment(self.api, self.user_id)  # Added Equipment class
        self.events = self.Events(self.api, self.user_id)  # Added Events class
        self.gym = self.Gym(self.api, self.user_id)  # Added Gym class
        self.hof = self.HallOfFame(self.api, self.user_id)  # Added HallOfFame class
        self.honors = self.Honors(self.api, self.user_id)  # Added Honors class
        self.icons = self.Icons(self.api, self.user_id)  # Added Icons class
        self.jobpoints = self.JobPoints(self.api, self.user_id)  # Added JobPoints class
        self.log = self.Log(self.api, self.user_id)  # Added Log class

        logger.info(f"Initialized User with ID: {self.user_id}")


    class Ammo:
        def __init__(self, api: TornAPI, user_id: Optional[int]):
            self.api = api
            self.user_id = user_id
            self.ammo_data = None
            logger.info(f"Initialized Ammo for User ID: {self.user_id}")

        def fetch_ammo(self):
            """Fetch ammo data from the API."""
            logger.debug(f"Fetching ammo data for User ID: {self.user_id}")
            response = self.api.make_request('user', self.user_id, 'ammo')
            if response and 'ammo' in response:
                logger.info(f"Ammo data fetched for User ID: {self.user_id}")
                return [self.AmmoItem(item) for item in response['ammo']]
            logger.warning(f"No ammo data found for User ID: {self.user_id}")
            return []

        class AmmoItem:
            """Class representing an individual ammo item."""
            def __init__(self, data: Dict[str, Any]):
                self.ammo_id = data.get('ID', 0)
                self.equipped = bool(data.get('equipped', 0))
                self.quantity = data.get('quantity', 0)
                self.size = data.get('size', '')
                self.type = data.get('type', '')
                self.type_id = data.get('typeID', 0)
                logger.debug(f"Processed AmmoItem: {self}")

            def __repr__(self):
                return (
                    f"AmmoItem(ammo_id={self.ammo_id}, equipped={self.equipped}, "
                    f"quantity={self.quantity}, size={self.size}, type={self.type}, type_id={self.type_id})"
                )

    class Basic:
        def __init__(self, api: TornAPI, user_id: Optional[int]):
            self.api = api
            self.user_id = user_id
            self.basic_data = None
            logger.info(f"Initialized Basic info for User ID: {self.user_id}")

        def fetch_basic(self):
            """Fetch basic user information from the API."""
            logger.debug(f"Fetching basic information for User ID: {self.user_id}")
            response = self.api.make_request('user', self.user_id, 'basic')
            if response:
                logger.info(f"Basic information fetched for User ID: {self.user_id}")
                return self.BasicInfo(response)
            logger.warning(f"No basic information found for User ID: {self.user_id}")
            return None

        class BasicInfo:
            """Class representing basic user information."""
            def __init__(self, data: Dict[str, Any]):
                self.gender = data.get('gender', '')
                self.level = data.get('level', 0)
                self.name = data.get('name', '')
                self.player_id = data.get('player_id', 0)
                self.status = self.Status(data.get('status', {}))
                logger.debug(f"Processed BasicInfo: {self}")

            class Status:
                """Class representing the user's status."""
                def __init__(self, status_data: Dict[str, Any]):
                    self.color = status_data.get('color', '')
                    self.description = status_data.get('description', '')
                    self.details = status_data.get('details', '')
                    self.state = status_data.get('state', '')
                    self.until = status_data.get('until', 0)
                    logger.debug(f"Processed Status: {self}")

                def __repr__(self):
                    return (
                        f"Status(color={self.color}, description={self.description}, "
                        f"details={self.details}, state={self.state}, until={self.until})"
                    )

            def __repr__(self):
                return (
                    f"BasicInfo(gender={self.gender}, level={self.level}, name={self.name}, "
                    f"player_id={self.player_id}, status={self.status})"
                )

    class Attacks:
        def __init__(self, api: TornAPI, user_id: Optional[int]):
            self.api = api
            self.user_id = user_id
            self.attacks_data = []
            logger.info(f"Initialized Attacks for User ID: {self.user_id}")

        def fetch_attacks(self, from_timestamp: Optional[int] = None, to_timestamp: Optional[int] = None, limit: Optional[int] = None):
            """Fetches the last 100 attacks with optional filtering."""
            logger.debug(f"Fetching attacks for User ID: {self.user_id} with filters from: {from_timestamp}, to: {to_timestamp}, limit: {limit}")

            parameters = {}
            if from_timestamp:
                parameters['from'] = from_timestamp
            if to_timestamp:
                parameters['to'] = to_timestamp
            if limit:
                parameters['limit'] = limit

            response = self.api.make_request('user', self.user_id, 'attacks', parameters)

            if response and 'attacks' in response:
                logger.info(f"Attacks data fetched for User ID: {self.user_id}")
                self.attacks_data = [self.Attack(item) for item in response['attacks'].values()]
                return self.attacks_data
            else:
                logger.warning(f"No attacks data found for User ID: {self.user_id}")
                return []

        class Attack:
            """Class representing an individual attack."""
            def __init__(self, data: Dict[str, Any]):
                self.attacker_faction = data.get('attacker_faction', 0)
                self.attacker_factionname = data.get('attacker_factionname', '')
                self.attacker_id = data.get('attacker_id', 0)
                self.attacker_name = data.get('attacker_name', '')
                self.chain = data.get('chain', 0)
                self.code = data.get('code', '')
                self.defender_faction = data.get('defender_faction', 0)
                self.defender_factionname = data.get('defender_factionname', '')
                self.defender_id = data.get('defender_id', 0)
                self.defender_name = data.get('defender_name', '')
                self.modifiers = data.get('modifiers', {})
                self.raid = bool(data.get('raid', 0))
                self.ranked_war = bool(data.get('ranked_war', 0))
                self.respect = data.get('respect', 0.0)
                self.respect_gain = data.get('respect_gain', 0.0)
                self.respect_loss = data.get('respect_loss', 0.0)
                self.result = data.get('result', '')
                self.stealthed = bool(data.get('stealthed', 0))
                self.timestamp_ended = data.get('timestamp_ended', 0)
                self.timestamp_started = data.get('timestamp_started', 0)
                logger.debug(f"Processed Attack: {self}")

            def __repr__(self):
                return (
                    f"Attack(attacker_name={self.attacker_name}, defender_name={self.defender_name}, "
                    f"respect_gain={self.respect_gain}, respect_loss={self.respect_loss}, result={self.result})"
                )

    class AttacksFull:
        def __init__(self, api: TornAPI, user_id: Optional[int]):
            self.api = api
            self.user_id = user_id
            self.attacksfull_data = []
            logger.info(f"Initialized AttacksFull for User ID: {self.user_id}")

        def fetch_attacksfull(self, from_timestamp: Optional[int] = None, to_timestamp: Optional[int] = None, limit: Optional[int] = None):
            """Fetches the last 1000 attacks with less details and optional filtering."""
            logger.debug(f"Fetching attacksfull for User ID: {self.user_id} with filters from: {from_timestamp}, to: {to_timestamp}, limit: {limit}")

            parameters = {}
            if from_timestamp:
                parameters['from'] = from_timestamp
            if to_timestamp:
                parameters['to'] = to_timestamp
            if limit:
                parameters['limit'] = limit

            response = self.api.make_request('user', self.user_id, 'attacksfull', parameters)

            if response and 'attacks' in response:
                logger.info(f"AttacksFull data fetched for User ID: {self.user_id}")
                self.attacksfull_data = [self.AttackFull(item) for item in response['attacks'].values()]
                return self.attacksfull_data
            else:
                logger.warning(f"No attacksfull data found for User ID: {self.user_id}")
                return []

        class AttackFull:
            """Class representing an individual attack with less details."""
            def __init__(self, data: Dict[str, Any]):
                self.attacker_faction = data.get('attacker_faction', 0)
                self.attacker_id = data.get('attacker_id', 0)
                self.code = data.get('code', '')
                self.defender_faction = data.get('defender_faction', 0)
                self.defender_id = data.get('defender_id', 0)
                self.respect = data.get('respect', 0.0)
                self.result = data.get('result', '')
                self.stealthed = bool(data.get('stealthed', 0))
                self.timestamp_ended = data.get('timestamp_ended', 0)
                self.timestamp_started = data.get('timestamp_started', 0)
                logger.debug(f"Processed AttackFull: {self}")

            def __repr__(self):
                return (
                    f"AttackFull(attacker_id={self.attacker_id}, defender_id={self.defender_id}, "
                    f"respect={self.respect}, result={self.result}, stealthed={self.stealthed})"
                )

    class Bars:
        def __init__(self, api: TornAPI, user_id: Optional[int]):
            self.api = api
            self.user_id = user_id
            self.bars_data = None
            logger.info(f"Initialized Bars for User ID: {self.user_id}")

        def fetch_bars(self):
            """Fetches the current bars (energy, happy, life, nerve, chain) from the API."""
            logger.debug(f"Fetching bars for User ID: {self.user_id}")

            response = self.api.make_request('user', self.user_id, 'bars')

            if response:
                logger.info(f"Bars data fetched for User ID: {self.user_id}")
                self.bars_data = self.BarsData(response)
                return self.bars_data
            else:
                logger.warning(f"No bars data found for User ID: {self.user_id}")
                return None

        class BarsData:
            """Class representing the user's bars data."""
            def __init__(self, data: Dict[str, Any]):
                self.chain = self.ChainBar(data.get('chain', {}))
                self.energy = self.Bar(data.get('energy', {}))
                self.happy = self.Bar(data.get('happy', {}))
                self.life = self.Bar(data.get('life', {}))
                self.nerve = self.Bar(data.get('nerve', {}))
                self.server_time = data.get('server_time', 0)
                logger.debug(f"Processed BarsData: {self}")

            class Bar:
                """Class representing a generic bar (energy, happy, life, nerve)."""
                def __init__(self, bar_data: Dict[str, Any]):
                    self.current = bar_data.get('current', 0)
                    self.fulltime = bar_data.get('fulltime', 0)
                    self.increment = bar_data.get('increment', 0)
                    self.interval = bar_data.get('interval', 0)
                    self.maximum = bar_data.get('maximum', 0)
                    self.ticktime = bar_data.get('ticktime', 0)
                    logger.debug(f"Processed Bar: {self}")

                def __repr__(self):
                    return (
                        f"Bar(current={self.current}, fulltime={self.fulltime}, "
                        f"increment={self.increment}, interval={self.interval}, "
                        f"maximum={self.maximum}, ticktime={self.ticktime})"
                    )

            class ChainBar:
                """Class representing the chain bar."""
                def __init__(self, chain_data: Dict[str, Any]):
                    self.cooldown = chain_data.get('cooldown', 0)
                    self.current = chain_data.get('current', 0)
                    self.maximum = chain_data.get('maximum', 0)
                    self.modifier = chain_data.get('modifier', 0.0)
                    self.timeout = chain_data.get('timeout', 0)
                    logger.debug(f"Processed ChainBar: {self}")

                def __repr__(self):
                    return (
                        f"ChainBar(cooldown={self.cooldown}, current={self.current}, "
                        f"maximum={self.maximum}, modifier={self.modifier}, timeout={self.timeout})"
                    )

            def __repr__(self):
                return (
                    f"BarsData(chain={self.chain}, energy={self.energy}, happy={self.happy}, "
                    f"life={self.life}, nerve={self.nerve}, server_time={self.server_time})"
                )

    class BattleStats:
        def __init__(self, api: TornAPI, user_id: Optional[int]):
            self.api = api
            self.user_id = user_id
            self.battle_stats_data = None
            logger.info(f"Initialized BattleStats for User ID: {self.user_id}")

        def fetch_battle_stats(self):
            """Fetches the battle stats and their modifiers from the API."""
            logger.debug(f"Fetching battle stats for User ID: {self.user_id}")

            response = self.api.make_request('user', self.user_id, 'battlestats')

            if response:
                logger.info(f"Battle stats data fetched for User ID: {self.user_id}")
                self.battle_stats_data = self.BattleStatsData(response)
                return self.battle_stats_data
            else:
                logger.warning(f"No battle stats data found for User ID: {self.user_id}")
                return None

        class BattleStatsData:
            """Class representing the user's battle stats and their modifiers."""
            def __init__(self, data: Dict[str, Any]):
                self.defense = data.get('defense', 0)
                self.defense_info = data.get('defense_info', [])
                self.defense_modifier = data.get('defense_modifier', 0)

                self.dexterity = data.get('dexterity', 0)
                self.dexterity_info = data.get('dexterity_info', [])
                self.dexterity_modifier = data.get('dexterity_modifier', 0)

                self.speed = data.get('speed', 0)
                self.speed_info = data.get('speed_info', [])
                self.speed_modifier = data.get('speed_modifier', 0)

                self.strength = data.get('strength', 0)
                self.strength_info = data.get('strength_info', [])
                self.strength_modifier = data.get('strength_modifier', 0)

                self.total = data.get('total', 0)

                logger.debug(f"Processed BattleStatsData: {self}")

            def __repr__(self):
                return (
                    f"BattleStatsData(defense={self.defense}, defense_modifier={self.defense_modifier}, "
                    f"defense_info={self.defense_info}, dexterity={self.dexterity}, "
                    f"dexterity_modifier={self.dexterity_modifier}, dexterity_info={self.dexterity_info}, "
                    f"speed={self.speed}, speed_modifier={self.speed_modifier}, "
                    f"speed_info={self.speed_info}, strength={self.strength}, "
                    f"strength_modifier={self.strength_modifier}, strength_info={self.strength_info}, "
                    f"total={self.total})"
                )

    class Bazaar:
        def __init__(self, api: TornAPI, user_id: Optional[int]):
            self.api = api
            self.user_id = user_id
            self.bazaar_items = None
            logger.info(f"Initialized Bazaar for User ID: {self.user_id}")

        def fetch_bazaar(self):
            """Fetches the bazaar items from the API."""
            logger.debug(f"Fetching bazaar items for User ID: {self.user_id}")
            response = self.api.make_request('user', self.user_id, 'bazaar')

            if response and 'bazaar' in response:
                logger.info(f"Bazaar data fetched for User ID: {self.user_id}")
                self.bazaar_items = [self.BazaarItem(item) for item in response['bazaar']]
                return self.bazaar_items
            else:
                logger.warning(f"No bazaar data found for User ID: {self.user_id}")
                return []

        class BazaarItem:
            """Class representing an individual bazaar item."""
            def __init__(self, data: Dict[str, Any]):
                self.id = data.get('ID', 0)
                self.market_price = data.get('market_price', 0)
                self.name = data.get('name', '')
                self.price = data.get('price', 0)
                self.quantity = data.get('quantity', 0)
                self.type = data.get('type', '')
                self.uid = data.get('UID', 0)
                logger.debug(f"Processed BazaarItem: {self}")

            def __repr__(self):
                return (
                    f"BazaarItem(id={self.id}, market_price={self.market_price}, name={self.name}, "
                    f"price={self.price}, quantity={self.quantity}, type={self.type}, uid={self.uid})"
                )

    class Cooldowns:
        # TODO look at the dictionatry return and see if its correct
        def __init__(self, api: TornAPI, user_id: Optional[int]):
            self.api = api
            self.user_id = user_id
            self.cooldowns_data = None
            logger.info(f"Initialized Cooldowns for User ID: {self.user_id}")

        def fetch_cooldowns(self):
            """Fetches the cooldown data from the API."""
            logger.debug(f"Fetching cooldowns for User ID: {self.user_id}")
            response = self.api.make_request('user', self.user_id, 'cooldowns')

            if response and 'cooldowns' in response:
                logger.info(f"Cooldown data fetched for User ID: {self.user_id}")
                return self.CooldownInfo(response['cooldowns'])
            else:
                logger.warning(f"No cooldown data found for User ID: {self.user_id}")
                return None

        class CooldownInfo:
            """Class representing cooldown information."""
            def __init__(self, data: Dict[str, Any]):
                self.booster = data.get('booster', 0)
                self.drug = data.get('drug', 0)
                self.medical = data.get('medical', 0)
                logger.debug(f"Processed CooldownInfo: {self}")

            def __repr__(self):
                return (
                    f"CooldownInfo(booster={self.booster}, drug={self.drug}, "
                    f"medical={self.medical})"
                )

    class Crimes:
        def __init__(self, api: TornAPI, user_id: Optional[int]):
            self.api = api
            self.user_id = user_id
            self.criminal_record = None
            logger.info(f"Initialized Crimes for User ID: {self.user_id}")

        def fetch_crimes(self):
            """Fetches the criminal record from the API."""
            logger.debug(f"Fetching crimes for User ID: {self.user_id}")
            response = self.api.make_request('user', self.user_id, 'crimes')

            if response and 'criminalrecord' in response:
                logger.info(f"Criminal record fetched for User ID: {self.user_id}")
                return self.CriminalRecord(response['criminalrecord'])
            else:
                logger.warning(f"No criminal record found for User ID: {self.user_id}")
                return None

        class CriminalRecord:
            """Class representing a user's criminal record."""
            def __init__(self, data: Dict[str, Any]):
                self.auto_theft = data.get('auto_theft', 0)
                self.computer_crimes = data.get('computer_crimes', 0)
                self.counterfeiting = data.get('counterfeiting', 0)
                self.cybercrime = data.get('cybercrime', 0)
                self.drug_deals = data.get('drug_deals', 0)
                self.extortion = data.get('extortion', 0)
                self.fraud = data.get('fraud', 0)
                self.fraud_crimes = data.get('fraud_crimes', 0)
                self.illegalproduction = data.get('illegalproduction', 0)
                self.illicitservices = data.get('illicitservices', 0)
                self.murder = data.get('murder', 0)
                self.other = data.get('other', 0)
                self.selling_illegal_products = data.get('selling_illegal_products', 0)
                self.theft = data.get('theft', 0)
                self.total = data.get('total', 0)
                self.vandalism = data.get('vandalism', 0)
                logger.debug(f"Processed CriminalRecord: {self}")

            def __repr__(self):
                return (
                    f"CriminalRecord(auto_theft={self.auto_theft}, computer_crimes={self.computer_crimes}, "
                    f"counterfeiting={self.counterfeiting}, cybercrime={self.cybercrime}, "
                    f"drug_deals={self.drug_deals}, extortion={self.extortion}, fraud={self.fraud}, "
                    f"fraud_crimes={self.fraud_crimes}, illegalproduction={self.illegalproduction}, "
                    f"illicitservices={self.illicitservices}, murder={self.murder}, other={self.other}, "
                    f"selling_illegal_products={self.selling_illegal_products}, theft={self.theft}, "
                    f"total={self.total}, vandalism={self.vandalism})"
                )

    class CriminalRecord:
        def __init__(self, api: TornAPI, user_id: Optional[int]):
            self.api = api
            self.user_id = user_id
            self.record_data = None
            logger.info(f"Initialized CriminalRecord for User ID: {self.user_id}")

        def fetch_record(self):
            """Fetches the current criminal record from the API."""
            logger.debug(f"Fetching criminal record for User ID: {self.user_id}")

            response = self.api.make_request('user', self.user_id, 'criminalrecord')

            if response:
                logger.info(f"Criminal record data fetched for User ID: {self.user_id}")
                self.record_data = self.RecordData(response['criminalrecord'])
                return self.record_data
            else:
                logger.warning(f"No criminal record found for User ID: {self.user_id}")
                return None

        class RecordData:
            """Class representing the user's criminal record data."""
            def __init__(self, data: Dict[str, Any]):
                self.auto_theft = data.get('auto_theft', 0)
                self.computer_crimes = data.get('computer_crimes', 0)
                self.counterfeiting = data.get('counterfeiting', 0)
                self.cybercrime = data.get('cybercrime', 0)
                self.drug_deals = data.get('drug_deals', 0)
                self.extortion = data.get('extortion', 0)
                self.fraud = data.get('fraud', 0)
                self.fraud_crimes = data.get('fraud_crimes', 0)
                self.illegal_production = data.get('illegalproduction', 0)
                self.illicit_services = data.get('illicitservices', 0)
                self.murder = data.get('murder', 0)
                self.other = data.get('other', 0)
                self.selling_illegal_products = data.get('selling_illegal_products', 0)
                self.theft = data.get('theft', 0)
                self.total = data.get('total', 0)
                self.vandalism = data.get('vandalism', 0)
                logger.debug(f"Processed RecordData: {self}")

            def __repr__(self):
                return (
                    f"RecordData(auto_theft={self.auto_theft}, "
                    f"computer_crimes={self.computer_crimes}, "
                    f"counterfeiting={self.counterfeiting}, "
                    f"cybercrime={self.cybercrime}, "
                    f"drug_deals={self.drug_deals}, "
                    f"extortion={self.extortion}, "
                    f"fraud={self.fraud}, "
                    f"fraud_crimes={self.fraud_crimes}, "
                    f"illegal_production={self.illegal_production}, "
                    f"illicit_services={self.illicit_services}, "
                    f"murder={self.murder}, "
                    f"other={self.other}, "
                    f"selling_illegal_products={self.selling_illegal_products}, "
                    f"theft={self.theft}, "
                    f"total={self.total}, "
                    f"vandalism={self.vandalism})"
                )

    class Discord:
        def __init__(self, api: TornAPI, user_id: Optional[int]):
            self.api = api
            self.user_id = user_id
            self.discord_data = None
            logger.info(f"Initialized Discord for User ID: {self.user_id}")

        def fetch_discord(self):
            """Fetches the current Discord verification information from the API."""
            logger.debug(f"Fetching Discord info for User ID: {self.user_id}")

            response = self.api.make_request('user', self.user_id, 'discord')

            if response and 'discord' in response:
                logger.info(f"Discord data fetched for User ID: {self.user_id}")
                self.discord_data = self.DiscordData(response['discord'])
                return self.discord_data
            else:
                logger.warning(f"No Discord data found for User ID: {self.user_id}")
                return None

        class DiscordData:
            """Class representing the user's Discord verification data."""
            def __init__(self, data: Dict[str, Any]):
                self.discord_id = data.get('discordID', '')
                self.user_id = data.get('userID', 0)
                logger.debug(f"Processed DiscordData: {self}")

            def __repr__(self):
                return f"DiscordData(discord_id='{self.discord_id}', user_id={self.user_id})"

    class DisplayItems:
            def __init__(self, api: TornAPI, user_id: Optional[int]):
                self.api = api
                self.user_id = user_id
                self.items = []
                logger.info(f"Initialized DisplayItems for User ID: {self.user_id}")

            def fetch_display(self):
                """Fetches the list of display items from the API."""
                logger.debug(f"Fetching display items for User ID: {self.user_id}")

                response = self.api.make_request('display', self.user_id)

                if response and 'display' in response:
                    logger.info(f"Display items fetched for User ID: {self.user_id}")
                    self.items = [self.DisplayItem(item) for item in response['display']]
                    return self.items
                else:
                    logger.warning(f"No display items found for User ID: {self.user_id}")
                    return []

            class DisplayItem:
                """Class representing an item in the display case."""
                def __init__(self, data: Dict[str, Any]):
                    self.circulation = data.get('circulation', 0)
                    self.id = data.get('ID', 0)
                    self.market_price = data.get('market_price', 0)
                    self.name = data.get('name', '')
                    self.quantity = data.get('quantity', 0)
                    self.type = data.get('type', '')
                    self.uid = data.get('UID', 0)
                    logger.debug(f"Processed DisplayItem: {self}")

                def __repr__(self):
                    return (f"DisplayItem(id={self.id}, name='{self.name}', "
                            f"quantity={self.quantity}, market_price={self.market_price}, "
                            f"circulation={self.circulation}, type='{self.type}', uid={self.uid})")
    
    class Education:
        def __init__(self, api: TornAPI, user_id: Optional[int]):
            self.api = api
            self.user_id = user_id
            self.education_completed = []
            self.education_current = None
            self.education_timeleft = None
            logger.info(f"Initialized Education for User ID: {self.user_id}")

        def fetch_education(self):
            """Fetches the user's education information from the API."""
            logger.debug(f"Fetching education info for User ID: {self.user_id}")

            response = self.api.make_request('user', self.user_id, 'education')

            if response:
                logger.info(f"Education data fetched for User ID: {self.user_id}")
                self.education_completed = response.get('education_completed', [])
                self.education_current = response.get('education_current', 0)
                self.education_timeleft = response.get('education_timeleft', 0)
                return self
            else:
                logger.warning(f"No education data found for User ID: {self.user_id}")
                return None

    class Equipment:
        def __init__(self, api: TornAPI, user_id: Optional[int]):
            self.api = api
            self.user_id = user_id
            self.equipped_items = []
            logger.info(f"Initialized Equipment for User ID: {self.user_id}")

        def fetch_equipment(self):
            """Fetches the list of equipped items from the API."""
            logger.debug(f"Fetching equipped items for User ID: {self.user_id}")

            response = self.api.make_request('user', self.user_id, 'equipment')

            if response and 'equipment' in response:
                logger.info(f"Equipped items fetched for User ID: {self.user_id}")
                self.equipped_items = [self.EquippedItem(item) for item in response['equipment']]
                return self.equipped_items
            else:
                logger.warning(f"No equipped items found for User ID: {self.user_id}")
                return []

        class EquippedItem:
            """Class representing an item equipped by the user."""
            def __init__(self, data: Dict[str, Any]):
                self.equipped = data.get('equipped', 0)
                self.id = data.get('ID', 0)
                self.market_price = data.get('market_price', 0)
                self.name = data.get('name', '')
                self.quantity = data.get('quantity', 1)  # Will always be 1
                self.type = data.get('type', '')
                self.uid = data.get('UID', 0)
                logger.debug(f"Processed EquippedItem: {self}")

            def __repr__(self):
                return (f"EquippedItem(id={self.id}, name='{self.name}', "
                        f"equipped_slot={self.equipped}, market_price={self.market_price}, "
                        f"quantity={self.quantity}, type='{self.type}', uid={self.uid})")

    class Events:
        def __init__(self, api: TornAPI, user_id: Optional[int]):
            self.api = api
            self.user_id = user_id
            self.event_list = []
            logger.info(f"Initialized Events for User ID: {self.user_id}")

        def fetch_events(self, limit: int = 25, from_timestamp: Optional[int] = None, to_timestamp: Optional[int] = None):
            """Fetches the last events for the user."""
            logger.debug(f"Fetching events for User ID: {self.user_id}, Limit: {limit}, From: {from_timestamp}, To: {to_timestamp}")

            parameters = {}
            if from_timestamp is not None:
                parameters['from'] = from_timestamp
            if to_timestamp is not None:
                parameters['to'] = to_timestamp
            if limit > 100:
                limit = 100  # Ensure limit does not exceed the maximum allowed
            parameters['limit'] = limit

            response = self.api.make_request('user', self.user_id, 'events', parameters)

            if response and 'events' in response:
                logger.info(f"Events fetched for User ID: {self.user_id}")
                self.event_list = [self.Event(event_uuid, event) for event_uuid, event in response['events'].items()]
                return self.event_list
            else:
                logger.warning(f"No events found for User ID: {self.user_id}")
                return []

        class Event:
            """Class representing a user event."""
            def __init__(self, event_uuid: str, data: Dict[str, Any]):
                self.event = data.get('event', '')
                self.timestamp = data.get('timestamp', 0)
                self.uuid = event_uuid  # Unique identifier for the event
                logger.debug(f"Processed Event: {self}")

            def __repr__(self):
                return f"Event(uuid='{self.uuid}', event='{self.event}', timestamp={self.timestamp})"

    class Gym:
        def __init__(self, api: TornAPI, user_id: Optional[int]):
            self.api = api
            self.user_id = user_id
            self.active_gym = None
            logger.info(f"Initialized Gym for User ID: {self.user_id}")

        def fetch_active_gym(self):
            """Fetches the currently active gym for the user."""
            logger.debug(f"Fetching active gym for User ID: {self.user_id}")

            response = self.api.make_request('user', self.user_id, 'gym')

            if response and 'active_gym' in response:
                logger.info(f"Active gym fetched for User ID: {self.user_id}")
                self.active_gym = response['active_gym']
                return self.active_gym
            else:
                logger.warning(f"No active gym found for User ID: {self.user_id}")
                return None

    class HallOfFame:
        def __init__(self, api: TornAPI, user_id: Optional[int]):
            self.api = api
            self.user_id = user_id
            self.rankings = {}
            logger.info(f"Initialized HallOfFame for User ID: {self.user_id}")

        def fetch_rankings(self):
            """Fetches the Hall of Fame rankings for the user."""
            logger.debug(f"Fetching Hall of Fame rankings for User ID: {self.user_id}")

            response = self.api.make_request('user', self.user_id, 'hof')

            if response and 'halloffame' in response:
                logger.info(f"Hall of Fame rankings fetched for User ID: {self.user_id}")
                self.rankings = {key: self.Ranking(value) for key, value in response['halloffame'].items()}
                return self.rankings
            else:
                logger.warning(f"No Hall of Fame data found for User ID: {self.user_id}")
                return {}

        class Ranking:
            """Class representing a ranking object."""
            def __init__(self, data: Dict[str, Any]):
                self.rank = data.get('rank', 0)
                self.value = data.get('value', 0)
                logger.debug(f"Processed Ranking: {self}")

            def __repr__(self):
                return f"Ranking(rank={self.rank}, value={self.value})"

    class Honors:
        def __init__(self, api: TornAPI, user_id: Optional[int]):
            self.api = api
            self.user_id = user_id
            self.honors_awarded = []
            self.honors_time = []
            logger.info(f"Initialized Honors for User ID: {self.user_id}")

        def fetch_honors(self):
            """Fetches the awarded honors for the user."""
            logger.debug(f"Fetching honors for User ID: {self.user_id}")

            response = self.api.make_request('user', self.user_id, 'honors')

            if response and 'honors_awarded' in response and 'honors_time' in response:
                logger.info(f"Honors fetched for User ID: {self.user_id}")
                self.honors_awarded = response['honors_awarded']
                self.honors_time = response['honors_time']
                return {
                    "awarded": self.honors_awarded,
                    "times": self.honors_time
                }
            else:
                logger.warning(f"No honors found for User ID: {self.user_id}")
                return {}

    class Icons:
        def __init__(self, api: TornAPI, user_id: Optional[int]):
            self.api = api
            self.user_id = user_id
            self.icons = {}
            logger.info(f"Initialized Icons for User ID: {self.user_id}")

        def fetch_icons(self):
            """Fetches the currently shown icons for the user."""
            logger.debug(f"Fetching icons for User ID: {self.user_id}")

            response = self.api.make_request('user', self.user_id, 'icons')

            if response and 'icons' in response:
                logger.info(f"Icons fetched for User ID: {self.user_id}")
                self.icons = response['icons']
                return self.icons
            else:
                logger.warning(f"No icons found for User ID: {self.user_id}")
                return {}

    class JobPoints:
        def __init__(self, api: TornAPI, user_id: Optional[int]):
            self.api = api
            self.user_id = user_id
            self.jobpoints_data = {}
            logger.info(f"Initialized JobPoints for User ID: {self.user_id}")

        def fetch_jobpoints(self):
            """Fetches the currently owned job points for the user."""
            logger.debug(f"Fetching job points for User ID: {self.user_id}")

            response = self.api.make_request('user', self.user_id, 'jobpoints')

            if response and 'jobpoints' in response:
                logger.info(f"Job points fetched for User ID: {self.user_id}")
                self.jobpoints_data = response['jobpoints']
                return self.jobpoints_data
            else:
                logger.warning(f"No job points found for User ID: {self.user_id}")
                return {}

    class Log:
        #TODO: Probably needs to be fully fleshed out to easily be able to access logs , basic implementation works 
        def __init__(self, api: TornAPI, user_id: Optional[int]):
            self.api = api
            self.user_id = user_id
            self.logs = {}
            logger.info(f"Initialized Log for User ID: {self.user_id}")

        def fetch_logs(self, parameters: Optional[dict] = None):
            """
            Fetches the last 100 activity logs for the user.

            Parameters:
            - parameters (Optional[dict]): A dictionary of query parameters to filter the logs.
                - 'from' (int): Limits results to logs with timestamps on or after this value.
                - 'to' (int): Limits results to logs with timestamps on or before this value.
                - 'log' (str): Comma-separated values to filter log types.
                - 'cat' (str): Comma-separated values to filter log categories.

            Returns:
            - dict: A dictionary containing the user's activity logs, or an empty dictionary if no logs are found.
            """
            logger.debug(f"Fetching logs for User ID: {self.user_id} with parameters: {parameters}")

            response = self.api.make_request('user', self.user_id, 'log', parameters)

            if response and 'log' in response:
                logger.info(f"Logs fetched for User ID: {self.user_id}")
                self.logs = response['log']
                return self.logs
            else:
                logger.warning(f"No logs found for User ID: {self.user_id}")
                return {}











class Sections:
    def __init__(self, api: TornAPI):
        self.api = api
        logger.info("Initialized Sections")

    def user(self, user_id: Optional[int] = None) -> User:
        """Return a User object initialized with the provided user_id."""
        logger.info(f"Creating User object for User ID: {user_id}")
        return User(self.api, user_id)

# Example usage
if __name__ == "__main__":
    api = TornAPI()
    sections = Sections(api)

    # Fetch user's basic info using user_id
    user = sections.user('')  # Replace with the actual user ID or None
    basic_info = user.basic.basic_data
    print(basic_info)

    # Close the logger
    close_logger(logger, file_handler)

    api.close()
