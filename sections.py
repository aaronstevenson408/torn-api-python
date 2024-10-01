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
        logger.info(f"Initialized User with ID: {self.user_id}")


    class Ammo:
        def __init__(self, api: TornAPI, user_id: Optional[int]):
            self.api = api
            self.user_id = user_id
            self.ammo_data = self._fetch_ammo()
            logger.info(f"Initialized Ammo for User ID: {self.user_id}")

        def _fetch_ammo(self):
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
            self.basic_data = self._fetch_basic()
            logger.info(f"Initialized Basic info for User ID: {self.user_id}")

        def _fetch_basic(self):
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
    user = sections.user(123456)  # Replace with the actual user ID or None
    basic_info = user.basic.basic_data
    print(basic_info)

    # Close the logger
    close_logger(logger, file_handler)

    api.close()
