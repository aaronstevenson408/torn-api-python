from typing import Dict, Any, Optional
from tornApi import TornAPI
from env_loader import load_environment_variables
from logger import setup_logger, close_logger

env = load_environment_variables()
if env is None:
    raise ValueError("Failed to load environment variables.")
logger, file_handler = setup_logger('Sections', env['DEBUG_LEVEL'])

class User:
    def __init__(self, api: TornAPI, user_id: Optional[int] = None):
        self.api = api
        self.user_id = user_id
        self.ammo = self.Ammo(self.api, self.user_id)
        self.basic = self.Basic(self.api, self.user_id)
        self.attacks = self.Attacks(self.api, self.user_id)
        self.attacks_full = self.AttacksFull(self.api, self.user_id)
        self.bars = self.Bars(self.api, self.user_id)
        self.battle_stats = self.BattleStats(self.api, self.user_id)
        self.bazaar = self.Bazaar(self.api, self.user_id)
        self.cooldowns = self.Cooldowns(self.api, self.user_id)
        self.crimes = self.Crimes(self.api, self.user_id)
        self.criminal_record = self.CriminalRecord(self.api, self.user_id)
        self.discord = self.Discord(self.api, self.user_id)
        self.display_items = self.DisplayItems(self.api, self.user_id)
        self.education = self.Education(self.api, self.user_id)
        self.equipment = self.Equipment(self.api, self.user_id)
        self.events = self.Events(self.api, self.user_id)
        self.gym = self.Gym(self.api, self.user_id)
        self.hof = self.HallOfFame(self.api, self.user_id)
        self.honors = self.Honors(self.api, self.user_id)
        self.icons = self.Icons(self.api, self.user_id)
        self.jobpoints = self.JobPoints(self.api, self.user_id)
        self.log = self.Log(self.api, self.user_id)
        self.lookup = self.Lookup(self.api)
        self.medals = self.Medals(self.api, self.user_id)
        self.merits = self.Merits(self.api, self.user_id)
        self.messages = self.Messages(self.api, self.user_id)
        self.missions = self.Missions(self.api, self.user_id)
        self.money = self.Money(self.api, self.user_id)
        self.networth = self.Networth(self.api, self.user_id)
        self.newevents = self.NewEvents(self.api, self.user_id)
        self.newmessages = self.NewMessages(self.api, self.user_id)
        self.notifications = self.Notifications(self.api, self.user_id)
        self.perks = self.Perks(self.api, self.user_id)
        self.personalstats = self.PersonalStats(self.api, self.user_id)
        self.profile = self.Profile(self.api, self.user_id)
        self.properties = self.Properties(self.api, self.user_id)
        self.public_status = self.PublicStatus(self.api, self.user_id)
        self.refills = self.Refills(self.api, self.user_id)
        self.reports = self.Reports(self.api, self.user_id)
        self.revives = self.Revives(self.api, self.user_id)
        self.revives_full = self.RevivesFull(self.api, self.user_id)
        self.skills = self.Skills(self.api, self.user_id)
        self.stocks = self.Stocks(self.api, self.user_id)
        self.timestamp = self.Timestamp(self.api, self.user_id)
        self.travel = self.Travel(self.api, self.user_id)
        self.weapon_exp = self.WeaponExp(self.api, self.user_id)
        self.work_stats = self.WorkStats(self.api, self.user_id)





        logger.info(f"Initialized User with ID: {self.user_id}")


    class Ammo:
        def __init__(self, api: TornAPI, user_id: Optional[int]):
            self.api = api
            self.user_id = user_id
            self.ammo_data = None
            logger.info(f"Initialized Ammo for User ID: {self.user_id}")

        def fetch_data(self):
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
                self.ammo_id = data.get('ammoID', 0)
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

        def __repr__(self):
            return f"Ammo(user_id={self.user_id}, ammo_data={self.ammo_data})"
        
    class Basic:
        def __init__(self, api: TornAPI, user_id: Optional[int]):
            self.api = api
            self.user_id = user_id
            self.basic_data = None
            logger.info(f"Initialized Basic info for User ID: {self.user_id}")

        def fetch_data(self):
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

        def fetch_data(self, from_timestamp: Optional[int] = None, to_timestamp: Optional[int] = None, limit: Optional[int] = None):
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
            self.attacks_full_data = []
            logger.info(f"Initialized AttacksFull for User ID: {self.user_id}")

        def fetch_data(self, from_timestamp: Optional[int] = None, to_timestamp: Optional[int] = None, limit: Optional[int] = None):
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

        def fetch_data(self):
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

        def fetch_data(self):
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

        def fetch_data(self):
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

        def fetch_data(self):
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

        def fetch_data(self):
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

        def fetch_data(self):
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

        def fetch_data(self):
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

            def fetch_data(self):
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

        def fetch_data(self):
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

        def fetch_data(self):
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

        def fetch_data(self, limit: int = 25, from_timestamp: Optional[int] = None, to_timestamp: Optional[int] = None):
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
        
        def fetch_data(self):
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

        def fetch_data(self):
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

        def fetch_data(self):
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

        def fetch_data(self):
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

        def fetch_data(self):
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

        def fetch_data(self, parameters: Optional[dict] = None):
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

    class Lookup:
        #TODO Probably needs to return an object but returns a list for right now
        def __init__(self, api: TornAPI):
            self.api = api
            self.selections = []  # Initialize as an empty list
            logger.info("Initialized Lookup:")

        def fetch_data(self):
            """
            Fetches a list of all available selections in the API and stores them in self.selections.

            Returns:
            - list: A list of strings representing the available selections.
            """
            logger.debug("Fetching all selections from the API.")

            response = self.api.make_request('user', None, 'lookup')

            if response and 'selections' in response:
                self.selections = response['selections']  # Save fetched selections
                logger.info("Selections fetched and stored successfully.")
                return self.selections
            else:
                logger.warning("No selections found.")
                return []

    class Medals:
        def __init__(self, api: TornAPI, user_id: Optional[int]):
            self.api = api
            self.user_id = user_id
            self.medals_awarded = []
            self.medals_time = []
            logger.info(f"Initialized Medals for User ID: {self.user_id}")

        def fetch_data(self):
            """
            Fetches the awarded medals of a player, along with the times when they were awarded.

            Returns:
            - dict: A dictionary with 'medals_awarded' (list of integers) and 'medals_time' (list of timestamps).
            """
            logger.debug(f"Fetching medals for User ID: {self.user_id}")

            response = self.api.make_request('user', self.user_id, 'medals')

            if response and 'medals_awarded' in response and 'medals_time' in response:
                self.medals_awarded = response['medals_awarded']
                self.medals_time = response['medals_time']
                logger.info(f"Medals fetched for User ID: {self.user_id}")
                return {
                    'medals_awarded': self.medals_awarded,
                    'medals_time': self.medals_time
                }
            else:
                logger.warning(f"No medals found for User ID: {self.user_id}")
                return {}

    class Merits:
        def __init__(self, api: TornAPI, user_id: Optional[int]):
            self.api = api
            self.user_id = user_id
            self.merits_data = None
            logger.info(f"Initialized Merits for User ID: {self.user_id}")

        def fetch_data(self):
            """
            Fetches the player's assigned merits and sets them as attributes in the MeritsData class.

            Returns:
            - MeritsData: An instance of the MeritsData class containing the player's merits.
            """
            logger.debug(f"Fetching merits for User ID: {self.user_id}")

            response = self.api.make_request('user', self.user_id, 'merits')

            if response and 'merits' in response:
                self.merits_data = self.MeritsData(response['merits'])
                logger.info(f"Merits fetched and processed for User ID: {self.user_id}")
                return self.merits_data
            else:
                logger.warning(f"No merits data found for User ID: {self.user_id}")
                return None

        class MeritsData:
            """
            A class representing the player's assigned merits, where each merit is an attribute.
            """
            def __init__(self, merits: Dict[str, int]):
                # Assign each merit type as an attribute
                self.addiction_mitigation = merits.get('Addiction Mitigation', 0)
                self.awareness = merits.get('Awareness', 0)
                self.bank_interest = merits.get('Bank Interest', 0)
                self.brawn = merits.get('Brawn', 0)
                self.club_mastery = merits.get('Club Mastery', 0)
                self.crime_xp = merits.get('Crime XP', 0)
                self.critical_hit_rate = merits.get('Critical Hit Rate', 0)
                self.education_length = merits.get('Education Length', 0)
                self.employee_effectiveness = merits.get('Employee Effectiveness', 0)
                self.evasion = merits.get('Evasion', 0)
                self.heavy_artillery_mastery = merits.get('Heavy Artillery Mastery', 0)
                self.hospitalizing = merits.get('Hospitalizing', 0)
                self.life_points = merits.get('Life Points', 0)
                self.machine_gun_mastery = merits.get('Machine Gun Mastery', 0)
                self.masterful_looting = merits.get('Masterful Looting', 0)
                self.mechanical_mastery = merits.get('Mechanical Mastery', 0)
                self.nerve_bar = merits.get('Nerve Bar', 0)
                self.piercing_mastery = merits.get('Piercing Mastery', 0)
                self.pistol_mastery = merits.get('Pistol Mastery', 0)
                self.protection = merits.get('Protection', 0)
                self.rifle_mastery = merits.get('Rifle Mastery', 0)
                self.sharpness = merits.get('Sharpness', 0)
                self.shotgun_mastery = merits.get('Shotgun Mastery', 0)
                self.slashing_mastery = merits.get('Slashing Mastery', 0)
                self.smg_mastery = merits.get('SMG Mastery', 0)
                self.stealth = merits.get('Stealth', 0)
                self.temporary_mastery = merits.get('Temporary Mastery', 0)
                logger.debug(f"Processed MeritsData: {self}")

            def __repr__(self):
                return (f"MeritsData(Addiction Mitigation={self.addiction_mitigation}, Awareness={self.awareness}, "
                        f"Bank Interest={self.bank_interest}, Brawn={self.brawn}, Club Mastery={self.club_mastery}, "
                        f"Crime XP={self.crime_xp}, Critical Hit Rate={self.critical_hit_rate}, "
                        f"Education Length={self.education_length}, Employee Effectiveness={self.employee_effectiveness}, "
                        f"Evasion={self.evasion}, Heavy Artillery Mastery={self.heavy_artillery_mastery}, "
                        f"Hospitalizing={self.hospitalizing}, Life Points={self.life_points}, "
                        f"Machine Gun Mastery={self.machine_gun_mastery}, Masterful Looting={self.masterful_looting}, "
                        f"Mechanical Mastery={self.mechanical_mastery}, Nerve Bar={self.nerve_bar}, "
                        f"Piercing Mastery={self.piercing_mastery}, Pistol Mastery={self.pistol_mastery}, "
                        f"Protection={self.protection}, Rifle Mastery={self.rifle_mastery}, "
                        f"Sharpness={self.sharpness}, Shotgun Mastery={self.shotgun_mastery}, "
                        f"Slashing Mastery={self.slashing_mastery}, SMG Mastery={self.smg_mastery}, "
                        f"Stealth={self.stealth}, Temporary Mastery={self.temporary_mastery})")

    class Messages:
        def __init__(self, api: TornAPI, user_id: Optional[int]):
            self.api = api
            self.user_id = user_id
            self.messages_data = None
            logger.info(f"Initialized Messages for User ID: {self.user_id}")

        def fetch_data(self, from_timestamp: Optional[int] = None, to_timestamp: Optional[int] = None, limit: Optional[int] = None):
            """
            Fetch the user's messages based on optional filters (from, to, limit).
            
            Parameters:
            - from_timestamp (Optional[int]): Limits results to have their timestamp after or on this timestamp.
            - to_timestamp (Optional[int]): Limits results to have their timestamp before or on this timestamp.
            - limit (Optional[int]): Limits the amount of results. Will use the default if above the allowed amount.
            
            Returns:
            - List[Message]: A list of message objects.
            """
            logger.debug(f"Fetching messages for User ID: {self.user_id}")

            # Construct query parameters
            parameters = {}
            if from_timestamp:
                parameters['from'] = from_timestamp
            if to_timestamp:
                parameters['to'] = to_timestamp
            if limit:
                parameters['limit'] = limit

            # Make API request
            response = self.api.make_request('user', self.user_id, 'messages', parameters)

            if response and 'messages' in response:
                self.messages_data = {msg_id: self.Message(msg_id, msg_data) for msg_id, msg_data in response['messages'].items()}
                logger.info(f"Fetched {len(self.messages_data)} messages for User ID: {self.user_id}")
                return self.messages_data
            else:
                logger.warning(f"No messages data found for User ID: {self.user_id}")
                return None

        class Message:
            """
            A class representing an individual message.
            """
            def __init__(self, msg_id: int, data: Dict[str, Any]):
                self.id = msg_id
                self.name = data.get('name', '')
                self.read = bool(data.get('read', 0))
                self.seen = bool(data.get('seen', 0))
                self.timestamp = data.get('timestamp', 0)
                self.title = data.get('title', '')
                self.type = data.get('type', '')

            def __repr__(self):
                return (f"Message(ID={self.id}, Name='{self.name}', Read={self.read}, Seen={self.seen}, "
                        f"Timestamp={self.timestamp}, Title='{self.title}', Type='{self.type}')")

    class Missions:
        def __init__(self, api: TornAPI, user_id: Optional[int]):
            self.api = api
            self.user_id = user_id
            self.missions_data = None
            logger.info(f"Initialized Missions for User ID: {self.user_id}")

        def fetch_data(self):
            """
            Fetch the user's missions information.

            Returns:
            - Dict[str, List[Mission]]: A dictionary where each key is a mission giver (e.g., 'Duke'),
              and the value is a list of Mission objects.
            """
            logger.debug(f"Fetching missions for User ID: {self.user_id}")
            
            # Make API request
            response = self.api.make_request('user', self.user_id, 'missions')

            if response and 'missions' in response:
                self.missions_data = {mission_giver: [self.Mission(mission_data) for mission_data in missions]
                                      for mission_giver, missions in response['missions'].items()}
                logger.info(f"Fetched missions for User ID: {self.user_id}")
                return self.missions_data
            else:
                logger.warning(f"No missions data found for User ID: {self.user_id}")
                return None

        class Mission:
            """
            A class representing an individual mission.
            """
            def __init__(self, data: Dict[str, Any]):
                self.status = data.get('status', 'notAccepted')
                self.title = data.get('title', '')

            def __repr__(self):
                return f"Mission(status='{self.status}', title='{self.title}')"

    class Money:
        def __init__(self, api: TornAPI, user_id: Optional[int]):
            self.api = api
            self.user_id = user_id
            self.money_data = None
            logger.info(f"Initialized Money for User ID: {self.user_id}")

        def fetch_data(self):
            """
            Fetch the user's money information.

            Returns:
            - MoneyData: An instance of MoneyData containing various financial details of the user.
            """
            logger.debug(f"Fetching money information for User ID: {self.user_id}")
            
            # Make API request
            response = self.api.make_request('user', self.user_id, 'money')

            if response:
                self.money_data = self.MoneyData(response)
                logger.info(f"Fetched money data for User ID: {self.user_id}")
                return self.money_data
            else:
                logger.warning(f"No money data found for User ID: {self.user_id}")
                return None

        class MoneyData:
            """
            A class representing the user's financial information.
            """
            def __init__(self, data: Dict[str, Any]):
                self.cayman_bank = data.get('cayman_bank', 0)
                self.city_bank = self.CityBank(data.get('city_bank', {}))
                self.company_funds = data.get('company_funds', 0)
                self.daily_networth = data.get('daily_networth', 0)
                self.money_onhand = data.get('money_onhand', 0)
                self.points = data.get('points', 0)
                self.vault_amount = data.get('vault_amount', 0)
                logger.debug(f"Processed MoneyData: {self}")

            def __repr__(self):
                return (f"MoneyData(cayman_bank={self.cayman_bank}, city_bank={self.city_bank}, "
                        f"company_funds={self.company_funds}, daily_networth={self.daily_networth}, "
                        f"money_onhand={self.money_onhand}, points={self.points}, vault_amount={self.vault_amount})")

            class CityBank:
                """
                A class representing the user's City Bank information.
                """
                def __init__(self, data: Dict[str, Any]):
                    self.amount = data.get('amount', 0)
                    self.time_left = data.get('time_left', 0)

                def __repr__(self):
                    return f"CityBank(amount={self.amount}, time_left={self.time_left})"

    class Networth:
        def __init__(self, api: TornAPI, user_id: Optional[int]):
            self.api = api
            self.user_id = user_id
            self.networth_data = None
            logger.info(f"Initialized Networth for User ID: {self.user_id}")

        def fetch_data(self):
            """
            Fetch the user's live networth values.

            Returns:
            - NetworthData: An instance of NetworthData containing the user's financial assets and their corresponding values.
            """
            logger.debug(f"Fetching networth information for User ID: {self.user_id}")

            # Make API request
            response = self.api.make_request('user', self.user_id, 'networth')

            if response:
                self.networth_data = self.NetworthData(response.get('networth', {}))
                logger.info(f"Fetched networth data for User ID: {self.user_id}")
                return self.networth_data
            else:
                logger.warning(f"No networth data found for User ID: {self.user_id}")
                return None

        class NetworthData:
            """
            A class representing the user's networth values.
            """
            def __init__(self, data: Dict[str, Any]):
                self.auctionhouse = data.get('auctionhouse', 0)
                self.bank = data.get('bank', 0)
                self.bazaar = data.get('bazaar', 0)
                self.bookie = data.get('bookie', 0)
                self.cayman = data.get('cayman', 0)
                self.company = data.get('company', 0)
                self.displaycase = data.get('displaycase', 0)
                self.enlistedcars = data.get('enlistedcars', 0)
                self.itemmarket = data.get('itemmarket', 0)
                self.items = data.get('items', 0)
                self.loan = data.get('loan', 0)
                self.parsetime = data.get('parsetime', 0.0)
                self.pending = data.get('pending', 0)
                self.piggybank = data.get('piggybank', 0)
                self.points = data.get('points', 0)
                self.properties = data.get('properties', 0)
                self.stockmarket = data.get('stockmarket', 0)
                self.total = data.get('total', 0)
                self.trade = data.get('trade', 0)
                self.unpaidfees = data.get('unpaidfees', 0)
                self.vault = data.get('vault', 0)
                self.wallet = data.get('wallet', 0)
                logger.debug(f"Processed NetworthData: {self}")

            def __repr__(self):
                return (
                    f"NetworthData(auctionhouse={self.auctionhouse}, bank={self.bank}, "
                    f"bazaar={self.bazaar}, bookie={self.bookie}, cayman={self.cayman}, "
                    f"company={self.company}, displaycase={self.displaycase}, enlistedcars={self.enlistedcars}, "
                    f"itemmarket={self.itemmarket}, items={self.items}, loan={self.loan}, "
                    f"parsetime={self.parsetime}, pending={self.pending}, piggybank={self.piggybank}, "
                    f"points={self.points}, properties={self.properties}, stockmarket={self.stockmarket}, "
                    f"total={self.total}, trade={self.trade}, unpaidfees={self.unpaidfees}, vault={self.vault}, "
                    f"wallet={self.wallet})"
                )

    class NewEvents:
        def __init__(self, api: TornAPI, user_id: Optional[int]):
            self.api = api
            self.user_id = user_id
            self.events_data = None
            logger.info(f"Initialized NewEvents for User ID: {self.user_id}")

        def fetch_data(self):
            """
            Fetch the user's last 100 unread events.

            Returns:
            - NewEventsData: An instance of NewEventsData containing the user's unread events.
            """
            logger.debug(f"Fetching new events for User ID: {self.user_id}")

            # Make API request
            response = self.api.make_request('user', self.user_id, 'newevents')

            if response:
                self.events_data = self.NewEventsData(response)
                logger.info(f"Fetched new events for User ID: {self.user_id}")
                return self.events_data
            else:
                logger.warning(f"No new events data found for User ID: {self.user_id}")
                return None

        class NewEventsData:
            """
            A class representing the user's unread events.
            """
            def __init__(self, data: Dict[str, Any]):
                self.events = {event_id: self.Event(event_data) for event_id, event_data in data.get('events', {}).items()}
                self.player_id = data.get('player_id', 0)
                logger.debug(f"Processed NewEventsData: {self}")

            class Event:
                """
                A class representing an individual event.
                """
                def __init__(self, data: Dict[str, Any]):
                    self.event = data.get('event', '')
                    self.seen = data.get('seen', 0)  # Will always be 0 for unread events
                    self.timestamp = data.get('timestamp', 0)
                    logger.debug(f"Processed Event: {self}")

                def __repr__(self):
                    return f"Event(event='{self.event}', seen={self.seen}, timestamp={self.timestamp})"

            def __repr__(self):
                return f"NewEventsData(events={self.events}, player_id={self.player_id})"

    class NewMessages:
        def __init__(self, api: TornAPI, user_id: Optional[int]):
            self.api = api
            self.user_id = user_id
            self.messages_data = None
            logger.info(f"Initialized NewMessages for User ID: {self.user_id}")

        def fetch_data(self):
            """
            Fetch the user's unread messages.

            Returns:
            - NewMessagesData: An instance of NewMessagesData containing the user's unread messages.
            """
            logger.debug(f"Fetching new messages for User ID: {self.user_id}")

            # Make API request
            response = self.api.make_request('user', self.user_id, 'newmessages')

            if response:
                self.messages_data = self.NewMessagesData(response)
                logger.info(f"Fetched new messages for User ID: {self.user_id}")
                return self.messages_data
            else:
                logger.warning(f"No new messages data found for User ID: {self.user_id}")
                return None

        class NewMessagesData:
            """
            A class representing the user's unread messages.
            """
            def __init__(self, data: Dict[str, Any]):
                self.messages = {message_id: self.Message(message_data) for message_id, message_data in data.get('messages', {}).items()}
                self.player_id = data.get('player_id', 0)
                logger.debug(f"Processed NewMessagesData: {self}")

            class Message:
                """
                A class representing an individual message.
                """
                def __init__(self, data: Dict[str, Any]):
                    self.ID = data.get('ID', 0)
                    self.name = data.get('name', '')
                    self.read = data.get('read', 0)  # Will always be 0 for unread messages
                    self.seen = data.get('seen', 0)
                    self.timestamp = data.get('timestamp', 0)
                    self.title = data.get('title', '')
                    self.type = data.get('type', '')
                    logger.debug(f"Processed Message: {self}")

                def __repr__(self):
                    return (f"Message(ID={self.ID}, name='{self.name}', read={self.read}, "
                            f"seen={self.seen}, timestamp={self.timestamp}, title='{self.title}', "
                            f"type='{self.type}')")

            def __repr__(self):
                return f"NewMessagesData(messages={self.messages}, player_id={self.player_id})"

    class Notifications:
        def __init__(self, api: TornAPI, user_id: Optional[int]):
            self.api = api
            self.user_id = user_id
            self.notifications_data = None
            logger.info(f"Initialized Notifications for User ID: {self.user_id}")

        def fetch_data(self):
            """
            Fetch the user's notifications count.

            Returns:
            - NotificationsData: An instance of NotificationsData containing the counts of various notifications.
            """
            logger.debug(f"Fetching notifications for User ID: {self.user_id}")

            # Make API request
            response = self.api.make_request('user', self.user_id, 'notifications')

            if response:
                self.notifications_data = self.NotificationsData(response)
                logger.info(f"Fetched notifications for User ID: {self.user_id}")
                return self.notifications_data
            else:
                logger.warning(f"No notifications data found for User ID: {self.user_id}")
                return None

        class NotificationsData:
            """
            A class representing the counts of various notifications for the user.
            """
            def __init__(self, data: Dict[str, Any]):
                self.awards = data.get('awards', 0)
                self.competition = data.get('competition', 0)
                self.events = data.get('events', 0)
                self.messages = data.get('messages', 0)
                logger.debug(f"Processed NotificationsData: {self}")

            def __repr__(self):
                return (f"NotificationsData(awards={self.awards}, "
                        f"competition={self.competition}, events={self.events}, "
                        f"messages={self.messages})")

    class Perks:
        def __init__(self, api: TornAPI, user_id: Optional[int]):
            self.api = api
            self.user_id = user_id
            self.perks_data = None
            logger.info(f"Initialized Perks for User ID: {self.user_id}")

        def fetch_data(self):
            """
            Fetch the user's active perks.

            Returns:
            - PerksData: An instance of PerksData containing the user's active perks.
            """
            logger.debug(f"Fetching perks for User ID: {self.user_id}")

            # Make API request
            response = self.api.make_request('user', self.user_id, 'perks')

            if response:
                self.perks_data = self.PerksData(response)
                logger.info(f"Fetched perks for User ID: {self.user_id}")
                return self.perks_data
            else:
                logger.warning(f"No perks data found for User ID: {self.user_id}")
                return None

        class PerksData:
            """
            A class representing the user's active perks.
            """
            def __init__(self, data: Dict[str, Any]):
                self.book_perks = data.get('book_perks', [])
                self.education_perks = data.get('education_perks', [])
                self.enhancer_perks = data.get('enhancer_perks', [])
                self.faction_perks = data.get('faction_perks', [])
                self.job_perks = data.get('job_perks', [])
                self.merit_perks = data.get('merit_perks', [])
                self.property_perks = data.get('property_perks', [])
                self.stock_perks = data.get('stock_perks', [])
                logger.debug(f"Processed PerksData: {self}")

            def __repr__(self):
                return (f"PerksData(book_perks={self.book_perks}, education_perks={self.education_perks}, "
                        f"enhancer_perks={self.enhancer_perks}, faction_perks={self.faction_perks}, "
                        f"job_perks={self.job_perks}, merit_perks={self.merit_perks}, "
                        f"property_perks={self.property_perks}, stock_perks={self.stock_perks})")

    class PersonalStats:
        # TODO: Needs to be double checked ( i believe that the update now works)
        def __init__(self, api: TornAPI, user_id: Optional[int]):
            self.api = api
            self.user_id = user_id
            self.stats_data = None
            logger.info(f"Initialized PersonalStats for User ID: {self.user_id}")

        def fetch_data(self, timestamp: Optional[int] = None, stat: Optional[str] = None):
            """
            Fetch the user's personal stats.
            
            Args:
            - timestamp (int, optional): The epoch timestamp to get the stats from. Older dates might return combined data.
            - stat (str, optional): The specific stat key to retrieve data for.
            
            Returns:
            - PersonalStatsData: An instance of PersonalStatsData containing the user's personal stats.
            """
            logger.debug(f"Fetching personal stats for User ID: {self.user_id}, Timestamp: {timestamp}, Stat: {stat}")
            
            # Prepare parameters for query
            parameters = {}
            if timestamp:
                parameters['timestamp'] = timestamp
            if stat:
                parameters['stat'] = stat

            # Make API request
            response = self.api.make_request('user', self.user_id, 'personalstats', parameters)
            # print(f"response {response}")
            if response and isinstance(response, dict) and 'personalstats' in response:
                # Create a new PersonalStatsData instance with the response data
                self.stats_data = self.PersonalStatsData(response['personalstats'])
                logger.info(f"Fetched personal stats for User ID: {self.user_id}")
                return self.stats_data
            else:
                logger.warning(f"No personal stats data found for User ID: {self.user_id}")
                return None

        class PersonalStatsData:
            """
            A class representing the user's personal stats.
            """
            def __init__(self, data: Dict[str, Any]):
                # Personal stats fields initialization
                self.activestreak = data.get('activestreak', 0)
                self.alcoholused = data.get('alcoholused', 0)
                self.argtravel = data.get('argtravel', 0)
                self.arrestsmade = data.get('arrestsmade', 0)
                self.attackcriticalhits = data.get('attackcriticalhits', 0)
                self.attackdamage = data.get('attackdamage', 0)
                self.attackhits = data.get('attackhits', 0)
                self.attackmisses = data.get('attackmisses', 0)
                self.attacksassisted = data.get('attacksassisted', 0)
                self.attacksdraw = data.get('attacksdraw', 0)
                self.attackslost = data.get('attackslost', 0)
                self.attacksstealthed = data.get('attacksstealthed', 0)
                self.attackswon = data.get('attackswon', 0)
                self.attackswonabroad = data.get('attackswonabroad', 0)
                self.auctionsells = data.get('auctionsells', 0)
                self.auctionswon = data.get('auctionswon', 0)
                self.awards = data.get('awards', 0)
                self.axehits = data.get('axehits', 0)
                self.bazaarcustomers = data.get('bazaarcustomers', 0)
                self.bazaarprofit = data.get('bazaarprofit', 0)
                self.bazaarsales = data.get('bazaarsales', 0)
                self.bestactivestreak = data.get('bestactivestreak', 0)
                self.bestdamage = data.get('bestdamage', 0)
                self.bestkillstreak = data.get('bestkillstreak', 0)
                self.bloodwithdrawn = data.get('bloodwithdrawn', 0)
                self.booksread = data.get('booksread', 0)
                self.boostersused = data.get('boostersused', 0)
                self.bountiescollected = data.get('bountiescollected', 0)
                self.bountiesplaced = data.get('bountiesplaced', 0)
                self.bountiesreceived = data.get('bountiesreceived', 0)
                self.candyused = data.get('candyused', 0)
                self.cantaken = data.get('cantaken', 0)
                self.cantravel = data.get('cantravel', 0)
                self.caytravel = data.get('caytravel', 0)
                self.chahits = data.get('chahits', 0)
                self.chitravel = data.get('chitravel', 0)
                self.cityfinds = data.get('cityfinds', 0)
                self.cityitemsbought = data.get('cityitemsbought', 0)
                self.classifiedadsplaced = data.get('classifiedadsplaced', 0)
                self.companymailssent = data.get('companymailssent', 0)
                self.consumablesused = data.get('consumablesused', 0)
                self.contractscompleted = data.get('contractscompleted', 0)
                self.counterfeiting = data.get('counterfeiting', 0)
                self.criminaloffenses = data.get('criminaloffenses', 0)
                self.cybercrime = data.get('cybercrime', 0)
                self.daysbeendonator = data.get('daysbeendonator', 0)
                self.defendslost = data.get('defendslost', 0)
                self.defendslostabroad = data.get('defendslostabroad', 0)
                self.defendsstalemated = data.get('defendsstalemated', 0)
                self.defendswon = data.get('defendswon', 0)
                self.defense = data.get('defense', 0)
                self.dexterity = data.get('dexterity', 0)
                self.drugsused = data.get('drugsused', 0)
                self.dubtravel = data.get('dubtravel', 0)
                self.dukecontractscompleted = data.get('dukecontractscompleted', 0)
                self.dumpfinds = data.get('dumpfinds', 0)
                self.dumpsearches = data.get('dumpsearches', 0)
                self.eastereggs = data.get('eastereggs', 0)
                self.eastereggsused = data.get('eastereggsused', 0)
                self.elo = data.get('elo', 0)
                self.endurance = data.get('endurance', 0)
                self.energydrinkused = data.get('energydrinkused', 0)
                self.extortion = data.get('extortion', 0)
                self.exttaken = data.get('exttaken', 0)
                self.factionmailssent = data.get('factionmailssent', 0)
                self.failedbusts = data.get('failedbusts', 0)
                self.fraud = data.get('fraud', 0)
                self.friendmailssent = data.get('friendmailssent', 0)
                self.grehits = data.get('grehits', 0)
                self.h2hhits = data.get('h2hhits', 0)
                self.hawtravel = data.get('hawtravel', 0)
                self.heahits = data.get('heahits', 0)
                self.highestbeaten = data.get('highestbeaten', 0)
                self.hollowammoused = data.get('hollowammoused', 0)
                self.hospital = data.get('hospital', 0)
                self.illegalproduction = data.get('illegalproduction', 0)
                self.illicitservices = data.get('illicitservices', 0)
                self.incendiaryammoused = data.get('incendiaryammoused', 0)
                self.intelligence = data.get('intelligence', 0)
                self.investedprofit = data.get('investedprofit', 0)
                self.itemsbought = data.get('itemsbought', 0)
                self.itemsboughtabroad = data.get('itemsboughtabroad', 0)
                self.itemsdumped = data.get('itemsdumped', 0)
                self.itemslooted = data.get('itemslooted', 0)
                self.itemssent = data.get('itemssent', 0)
                self.jailed = data.get('jailed', 0)
                self.japtravel = data.get('japtravel', 0)
                self.jobpointsused = data.get('jobpointsused', 0)
                self.kettaken = data.get('kettaken', 0)
                self.killstreak = data.get('killstreak', 0)
                self.largestmug = data.get('largestmug', 0)
                self.lontravel = data.get('lontravel', 0)
                self.lsdtaken = data.get('lsdtaken', 0)
                self.machits = data.get('machits', 0)
                self.mailssent = data.get('mailssent', 0)
                self.manuallabor = data.get('manuallabor', 0)
                self.medicalitemsused = data.get('medicalitemsused', 0)
                self.meritsbought = data.get('meritsbought', 0)
                self.mextravel = data.get('mextravel', 0)
                self.missioncreditsearned = data.get('missioncreditsearned', 0)
                self.missionscompleted = data.get('missionscompleted', 0)
                self.moneyinvested = data.get('moneyinvested', 0)
                self.moneymugged = data.get('moneymugged', 0)
                self.nerverefills = data.get('nerverefills', 0)
                self.networth = data.get('networth', 0)
                self.networthauctionhouse = data.get('networthauctionhouse', 0)
                self.networthbank = data.get('networthbank', 0)
                self.networthbazaar = data.get('networthbazaar', 0)
                self.networthbookie = data.get('networthbookie', 0)
                self.networthcayman = data.get('networthcayman', 0)
                self.networthcompany = data.get('networthcompany', 0)
                self.networthdisplaycase = data.get('networthdisplaycase', 0)
                self.networthenlistedcars = data.get('networthenlistedcars', 0)
                self.networthitemmarket = data.get('networthitemmarket', 0)
                self.networthitems = data.get('networthitems', 0)
                self.networthloan = data.get('networthloan', 0)
                self.networthpending = data.get('networthpending', 0)
                self.networthpiggybank = data.get('networthpiggybank', 0)
                self.networthpoints = data.get('networthpoints', 0)
                self.networthproperties = data.get('networthproperties', 0)
                self.networthstockmarket = data.get('networthstockmarket', 0)
                self.networthunpaidfees = data.get('networthunpaidfees', 0)
                self.networthvault = data.get('networthvault', 0)
                self.networthwallet = data.get('networthwallet', 0)
                self.onehitkills = data.get('onehitkills', 0)
                self.opitaken = data.get('opitaken', 0)
                self.organisedcrimes = data.get('organisedcrimes', 0)
                self.overdosed = data.get('overdosed', 0)
                self.pcptaken = data.get('pcptaken', 0)
                self.peoplebought = data.get('peoplebought', 0)
                self.peopleboughtspent = data.get('peopleboughtspent', 0)
                self.peoplebusted = data.get('peoplebusted', 0)
                self.personalsplaced = data.get('personalsplaced', 0)
                self.piehits = data.get('piehits', 0)
                self.piercingammoused = data.get('piercingammoused', 0)
                self.pishits = data.get('pishits', 0)
                self.pointsbought = data.get('pointsbought', 0)
                self.pointssold = data.get('pointssold', 0)
                self.racesentered = data.get('racesentered', 0)
                self.raceswon = data.get('raceswon', 0)
                self.racingpointsearned = data.get('racingpointsearned', 0)
                self.racingskill = data.get('racingskill', 0)
                self.raidhits = data.get('raidhits', 0)
                self.rankedwarhits = data.get('rankedwarhits', 0)
                self.rankedwarringwins = data.get('rankedwarringwins', 0)
                self.receivedbountyvalue = data.get('receivedbountyvalue', 0)
                self.refills = data.get('refills', 0)
                self.rehabcost = data.get('rehabcost', 0)
                self.rehabs = data.get('rehabs', 0)
                self.respectforfaction = data.get('respectforfaction', 0)
                self.retals = data.get('retals', 0)
                self.revives = data.get('revives', 0)
                self.reviveskill = data.get('reviveskill', 0)
                self.revivesreceived = data.get('revivesreceived', 0)
                self.rifhits = data.get('rifhits', 0)
                self.roundsfired = data.get('roundsfired', 0)
                self.shohits = data.get('shohits', 0)
                self.shrtaken = data.get('shrtaken', 0)
                self.slahits = data.get('slahits', 0)
                self.smghits = data.get('smghits', 0)
                self.soutravel = data.get('soutravel', 0)
                self.specialammoused = data.get('specialammoused', 0)
                self.speed = data.get('speed', 0)
                self.spetaken = data.get('spetaken', 0)
                self.spousemailssent = data.get('spousemailssent', 0)
                self.statenhancersused = data.get('statenhancersused', 0)
                self.stockfees = data.get('stockfees', 0)
                self.stocklosses = data.get('stocklosses', 0)
                self.stocknetprofits = data.get('stocknetprofits', 0)
                self.stockpayouts = data.get('stockpayouts', 0)
                self.stockprofits = data.get('stockprofits', 0)
                self.strength = data.get('strength', 0)
                self.switravel = data.get('switravel', 0)
                self.territoryclears = data.get('territoryclears', 0)
                self.territoryjoins = data.get('territoryjoins', 0)
                self.territorytime = data.get('territorytime', 0)
                self.theft = data.get('theft', 0)
                self.theyrunaway = data.get('theyrunaway', 0)
                self.tokenrefills = data.get('tokenrefills', 0)
                self.totalbountyreward = data.get('totalbountyreward', 0)
                self.totalbountyspent = data.get('totalbountyspent', 0)
                self.totalstats = data.get('totalstats', 0)
                self.totalworkingstats = data.get('totalworkingstats', 0)
                self.tracerammoused = data.get('tracerammoused', 0)
                self.trades = data.get('trades', 0)
                self.trainsreceived = data.get('trainsreceived', 0)
                self.traveltime = data.get('traveltime', 0)
                self.traveltimes = data.get('traveltimes', 0)
                self.unarmoredwon = data.get('unarmoredwon',0)
                self.useractivity = data.get('useractivity', 0)	
                self.victaken = data.get('victaken', 0)
                self.virusescoded = data.get('virusescoded', 0)
                self.weaponsbought = data.get('weaponsbought', 0)
                self.xantaken = data.get('xantaken', 0)
                self.yourunaway = data.get('yourunaway', 0)
                logger.debug(f"Processed PersonalStatsData: {self}")

            def __repr__(self):
                # Summary of some key stats for concise logging or printing
                return (f"PersonalStatsData(activestreak={self.activestreak}, alcoholused={self.alcoholused},"
                        f""
                        f"xantaken={self.xantaken}, yourunaway={self.yourunaway})")

    class Profile:
#TODO: needs to have a test for profile data  User.Profile:
        def __init__(self, api: TornAPI, user_id: Optional[int]):
            self.api = api
            self.user_id = user_id
            self.profile_data = None
            logger.info(f"Initialized Profile for User ID: {self.user_id}")

        def fetch_data(self):
            """
            Fetch the user's profile information.
            
            Returns:
            - ProfileData: An instance of ProfileData containing the user's profile.
            """
            logger.debug(f"Fetching profile for User ID: {self.user_id}")
            
            # Make API request
            response = self.api.make_request('user', self.user_id, 'profile')
            if response:
                self.profile_data = self.ProfileData(response)
                logger.info(f"Fetched profile for User ID: {self.user_id}")
                return self.profile_data
            else:
                logger.warning(f"No profile data found for User ID: {self.user_id}")
                return None

        class ProfileData:
            """
            A class representing the user's profile data.
            """
            def __init__(self, data: Dict[str, Any]):
                # Basic fields
                self.age = data.get('age', 0)
                self.awards = data.get('awards', 0)
                self.basicicons = self.Icons(data.get('basicicons', {}))
                self.competition = self.Competition(data.get('competition', {}))
                self.donator = data.get('donator', 0)
                self.enemies = data.get('enemies', 0)
                self.faction = self.Faction(data.get('faction', {}))
                self.forum_posts = data.get('forum_posts', 0)
                self.friends = data.get('friends', 0)
                self.gender = data.get('gender', 'Unknown')
                self.honor = data.get('honor', 0)
                self.job = self.Job(data.get('job', {}))
                self.karma = data.get('karma', 0)
                self.last_action = self.LastAction(data.get('last_action', {}))
                self.level = data.get('level', 0)
                self.life = self.Bar(data.get('life', {}))
                self.married = self.Married(data.get('married', {}))
                self.name = data.get('name', 'Unknown')
                self.player_id = data.get('player_id', None)
                self.profile_image = data.get('profile_image', '')
                self.property = data.get('property', '')
                self.property_id = data.get('property_id', 0)
                self.rank = data.get('rank', 'Unknown')
                self.revivable = data.get('revivable', 0)
                self.role = data.get('role', 'Unknown')
                self.signup = data.get('signup', 'Unknown')
                self.states = self.States(data.get('states', {}))
                self.status = self.Status(data.get('status', {}))
                logger.debug(f"Processed ProfileData: {self}")

            def __repr__(self):
                # Summary of some key profile fields for concise logging or printing
                return (f"ProfileData(name={self.name}, level={self.level}, "
                        f"faction={self.faction.faction_name}, life ={self.life.current} "
                        f"rank={self.rank}, status={self.status.state})")

            class Bar:
                def __init__(self, data: Dict[str, Any]):
                    self.current = data.get('current', 0)
                    self.fulltime = data.get('fulltime', 0)
                    self.increment = data.get('increment', 0)
                    self.interval = data.get('interval', 0)
                    self.maximum = data.get('maximum', 0)
                    self.ticktime = data.get('ticktime', 0)

            class Competition:
                def __init__(self, data: Dict[str, Any]):
                    self.attacks = data.get('attacks', 0)
                    self.image = data.get('image', '')
                    self.name = data.get('name', 'Unknown')
                    self.position = data.get('position', 'Unknown')
                    self.score = data.get('score', 0)
                    self.status = data.get('status', 'Unknown')
                    self.team = data.get('team', 'Unknown')
                    self.text = data.get('text', '')
                    self.total = data.get('total', 0)
                    self.treats_collected_total = data.get('treats_collected_total', 0)
                    self.votes = data.get('votes', 0)

            class Faction:
                def __init__(self, data: Dict[str, Any]):
                    self.days_in_faction = data.get('days_in_faction', 0)
                    self.faction_id = data.get('faction_id', 0)
                    self.faction_name = data.get('faction_name', '')
                    self.faction_tag = data.get('faction_tag', '')
                    self.position = data.get('position', '')

            class Icons:
                def __init__(self, data: Dict[str, Any]):
                    # Assuming the structure is a dictionary of icon IDs and their associated values
                    self.icons = data

            class Job:
                def __init__(self, data: Dict[str, Any]):
                    self.company_id = data.get('company_id', 0)
                    self.company_name = data.get('company_name', '')
                    self.company_type = data.get('company_type', 0)
                    self.job = data.get('job', '')
                    self.position = data.get('position', '')

            class LastAction:
                def __init__(self, data: Dict[str, Any]):
                    self.relative = data.get('relative', 'Unknown')
                    self.status = data.get('status', 'Offline')
                    self.timestamp = data.get('timestamp', 0)

            class Married:
                def __init__(self, data: Dict[str, Any]):
                    self.duration = data.get('duration', 0)
                    self.spouse_id = data.get('spouse_id', 0)
                    self.spouse_name = data.get('spouse_name', '')

            class States:
                def __init__(self, data: Dict[str, Any]):
                    self.hospital_timestamp = data.get('hospital_timestamp', 0)
                    self.jail_timestamp = data.get('jail_timestamp', 0)

            class Status:
                def __init__(self, data: Dict[str, Any]):
                    self.color = data.get('color', 'Unknown')
                    self.description = data.get('description', '')
                    self.details = data.get('details', '')
                    self.state = data.get('state', 'Okay')
                    self.until = data.get('until', 0)


#TODO: Needs to bee looked over and tested. modifications 
    class Properties:
        # Properties class manages the user's properties data.
        def __init__(self, api: TornAPI, user_id: Optional[int]):
            self.api = api
            self.user_id = user_id
            self.properties_data = None
            logger.info(f"Initialized Properties for User ID: {self.user_id}")

        def fetch_data(self):
            """
            Fetch the properties owned by the user and their spouse.
            
            Returns:
            - PropertiesData: An instance of PropertiesData containing the user's properties.
            """
            logger.debug(f"Fetching properties for User ID: {self.user_id}")
            
            try:
                # Make API request
                response = self.api.make_request('user', self.user_id, 'properties')
                logger.debug(f"API response for properties: {response}")
                
                # Check if the response contains the 'properties' field
                if not response or 'properties' not in response:
                    logger.warning(f"Properties not found in response for User ID: {self.user_id}")
                    return None

                # Parse and return properties data using the nested PropertiesData class
                self.properties_data = self.PropertiesData(response)
                logger.info(f"Fetched properties for User ID: {self.user_id}")
                return self.properties_data

            except Exception as e:
                logger.error(f"Error fetching properties for User ID: {self.user_id}: {e}")
                return None

        class PropertiesData:
            """
            Represents a collection of properties owned by the user.
            Each property has its own PropertyData object with further details.
            """
            def __init__(self, data: Dict[str, Any]):
                try:
                    # Parse properties into a list of Property instances
                    self.properties = [self.Property(prop_id, prop_data) for prop_id, prop_data in data.get('properties', {}).items()]
                    logger.debug(f"Processed PropertiesData with {len(self.properties)} properties.")
                except Exception as e:
                    logger.error(f"Error processing PropertiesData: {e}")

            def __repr__(self):
                # Summary for concise logging
                return f"PropertiesData with {len(self.properties)} properties"

            class Property:
                """
                Represents a single property and its associated data.
                Each property holds a PropertyData instance that contains its specific details.
                """
                def __init__(self, prop_id: str, data: Dict[str, Any]):
                    self.id = prop_id  # Store the property ID
                    self.property_data = self.PropertyData(
                        owner_id=data.get('owner_id', 0),
                        property_type=data.get('property_type', 'Unknown'),
                        property_name=data.get('property', 'Unknown'),
                        status=data.get('status', 'Unknown'),
                        happy=data.get('happy', 0),
                        upkeep=data.get('upkeep', 0),
                        staff_cost=data.get('staff_cost', 0),
                        cost=data.get('cost', 0),
                        marketprice=data.get('marketprice', 0),
                        modifications=self.Modifications(data.get('modifications', {})),
                        staff=self.Staff(data.get('staff', {})),
                        rented=self.Rented(data.get('rented', None)) if data.get('rented') else None
                    )
                    logger.debug(f"Processed Property ID: {self.id} ({self.property_data.property_name})")

                def __repr__(self):
                    return f"Property(ID: {self.id}, Name: {self.property_data.property_name})"

                class PropertyData:
                    """
                    Contains detailed information about a specific property.
                    """
                    from typing import Optional

                    def __init__(self, owner_id: int, property_type: str, property_name: str, status: str, 
                                happy: int, upkeep: int, staff_cost: int, cost: int, marketprice: int,
                                modifications: 'Property.Modifications', staff: 'Property.Staff', rented: Optional['Property.Rented']):
                        self.owner_id = owner_id
                        self.property_type = property_type
                        self.property_name = property_name
                        self.status = status
                        self.happy = happy
                        self.upkeep = upkeep
                        self.staff_cost = staff_cost
                        self.cost = cost
                        self.marketprice = marketprice
                        self.modifications = modifications
                        self.staff = staff
                        self.rented = rented

                    def __repr__(self):
                        return f"PropertyData(Name: {self.property_name}, Owner: {self.owner_id}, Status: {self.status})"

                class Modifications:
                    """
                    Represents modifications available in the property.
                    """
                    def __init__(self, data: Dict[str, Any]):
                        self.interior = data.get('interior', 0)
                        self.hot_tub = data.get('hot_tub', 0)
                        self.sauna = data.get('sauna', 0)
                        self.pool = data.get('pool', 0)
                        self.open_bar = data.get('open_bar', 0)
                        self.shooting_range = data.get('shooting_range', 0)
                        self.vault = data.get('vault', 0)
                        self.medical_facility = data.get('medical_facility', 0)
                        self.airstrip = data.get('airstrip', 0)
                        self.yacht = data.get('yacht', 0)

                class Rented:
                    """
                    Represents details about the property's rental status.
                    """
                    def __init__(self, data: Optional[Dict[str, Any]]):
                        self.cost_per_day = data.get('cost_per_day', 0)
                        self.days_left = data.get('days_left', 0)
                        self.total_cost = data.get('total_cost', 0)
                        self.user_id = data.get('user_id', 0)

                class Staff:
                    """
                    Represents the staff employed at the property.
                    """
                    def __init__(self, data: Dict[str, Any]):
                        self.maid = data.get('maid', 0)
                        self.guard = data.get('guard', 0)
                        self.pilot = data.get('pilot', 0)
                        self.butler = data.get('butler', 0)
                        self.doctor = data.get('doctor', 0)

    class PublicStatus:
        def __init__(self, api: TornAPI, user_id: Optional[int]):
            self.api = api
            self.user_id = user_id
            self.status_data = None
            logger.info(f"Initialized PublicStatus for User ID: {self.user_id}")

        def fetch_data(self):
            """
            Fetch the public status information of the user.
            
            Returns:
            - PublicStatusData: An instance of PublicStatusData containing the user's public status.
            """
            logger.debug(f"Fetching public status for User ID: {self.user_id}")
            
            try:
                # Make API request
                response = self.api.make_request('user', self.user_id, 'publicstatus')
                logger.debug(f"API response for public status: {response}")
                
                # Check if the response contains the necessary fields
                if not response or 'playername' not in response or 'status' not in response:
                    logger.warning(f"Public status information not found for User ID: {self.user_id}")
                    return None

                # Parse and return public status data
                self.status_data = self.PublicStatusData(response)
                logger.info(f"Fetched public status for User ID: {self.user_id}")
                return self.status_data

            except Exception as e:
                logger.error(f"Error fetching public status for User ID: {self.user_id}: {e}")
                return None

        class PublicStatusData:
            """
            A class representing the public status information of a user.
            """
            def __init__(self, data: Dict[str, Any]):
                try:
                    self.baned = data.get('baned', False)  # Note the intentional spelling from the API
                    self.playername = data.get('playername', 'Unknown')
                    self.status = data.get('status', 'Unknown')
                    self.user_id = data.get('userID', 0)
                    logger.debug(f"Processed PublicStatusData: {self}")
                except Exception as e:
                    logger.error(f"Error processing PublicStatusData: {e}")

            def __repr__(self):
                return f"PublicStatusData(playername={self.playername}, status={self.status}, user_id={self.user_id})"

    class Refills:
        def __init__(self, api: TornAPI, user_id: Optional[int]):
            self.api = api
            self.user_id = user_id
            self.refill_data = None
            logger.info(f"Initialized Refills for User ID: {self.user_id}")

        def fetch_data(self):
            """
            Fetch the refill status information for the user.

            Returns:
            - RefillsData: An instance of RefillsData containing the user's refill status.
            """
            logger.debug(f"Fetching refill status for User ID: {self.user_id}")
            
            try:
                # Make API request
                response = self.api.make_request('user', self.user_id, 'refills')
                logger.debug(f"API response for refill status: {response}")

                # Check if the response contains the necessary fields
                if not response or 'refills' not in response:
                    logger.warning(f"Refill status information not found for User ID: {self.user_id}")
                    return None

                # Parse and return refill data
                self.refill_data = self.RefillsData(response['refills'])
                logger.info(f"Fetched refill status for User ID: {self.user_id}")
                return self.refill_data

            except Exception as e:
                logger.error(f"Error fetching refill status for User ID: {self.user_id}: {e}")
                return None

        class RefillsData:
            """
            A class representing the refill status of a user.
            """
            def __init__(self, data: Dict[str, Any]):
                try:
                    self.energy_refill_used = data.get('energy_refill_used', False)
                    self.nerve_refill_used = data.get('nerve_refill_used', False)
                    self.special_refills_available = data.get('special_refills_available', 0)
                    self.token_refill_used = data.get('token_refill_used', False)
                    logger.debug(f"Processed RefillsData: {self}")
                except Exception as e:
                    logger.error(f"Error processing RefillsData: {e}")

            def __repr__(self):
                return (f"RefillsData(energy_refill_used={self.energy_refill_used}, "
                        f"nerve_refill_used={self.nerve_refill_used}, "
                        f"special_refills_available={self.special_refills_available}, "
                        f"token_refill_used={self.token_refill_used})")

    class Reports:
        # TODO: Needs to be tested (pretty sure that this doesnt work or returns null if you arent in a faction, test data seems to look good )
        def __init__(self, api: TornAPI, user_id: Optional[int]):
            self.api = api
            self.user_id = user_id
            self.reports_data = []
            logger.info(f"Initialized Reports for User ID: {self.user_id}")

        def fetch_data(self):
            """
            Fetch the last 100 reports for the user.

            Returns:
            - List[ReportData]: A list of ReportData instances containing report details.
            """
            logger.debug(f"Fetching last 100 reports for User ID: {self.user_id}")

            try:
                # Make API request
                response = self.api.make_request('user', self.user_id, 'reports')
                logger.debug(f"API response for reports: {response}")

                # Check if the response contains the necessary fields
                if not response or 'reports' not in response:
                    logger.warning(f"No reports found for User ID: {self.user_id}")
                    return []

                # Parse and return reports data
                self.reports_data = [self.ReportData(report) for report in response['reports']]
                logger.debug(f"reports data: {self.reports_data}")
                logger.info(f"Fetched {len(self.reports_data)} reports for User ID: {self.user_id}")
                return self.reports_data

            except Exception as e:
                logger.error(f"Error fetching reports for User ID: {self.user_id}: {e}")
                return []

        class ReportData:
            """
            A class representing the details of a report.
            """
            def __init__(self, data: Dict[str, Any]):
                self.id = data.get('id', '')
                self.target = data.get('target', 0)
                self.timestamp = data.get('timestamp', 0)
                self.type = data.get('type', '')
                self.user_id = data.get('user_id', 0)
                self.report = self.ReportDetails(data.get('report', {}))
                logger.debug(f"Processed ReportData: {self}")

            class ReportDetails:
                """
                A class representing the detailed information within a report.
                """
                def __init__(self, data: Dict[str, Any]):
                    self.bounties = data.get('bounties', [])
                    self.company_history = data.get('company_history', [])
                    self.defense = data.get('defense', 0)
                    self.dexterity = data.get('dexterity', 0)
                    self.enemylist = [self.UserData(user) for user in data.get('enemylist', [])]
                    self.faction_history = data.get('faction_history', [])
                    self.friendlist = [self.UserData(user) for user in data.get('friendlist', [])]
                    self.invested_amount = data.get('invested_amount', 0)
                    self.invested_completion = data.get('invested_completion', '')
                    self.money = data.get('money', 0)
                    self.otherlist = data.get('otherlist', [])
                    self.speed = data.get('speed', 0)
                    self.strength = data.get('strength', 0)
                    self.toplist = data.get('toplist', [])
                    self.total_battlestats = data.get('total_battlestats', 0)
                    self.truelevel = data.get('truelevel', 0)

            def __repr__(self):
                return (f"ReportData(id={self.id}, target={self.target}, "
                        f"timestamp={self.timestamp}, type={self.type}, "
                        f"user_id={self.user_id}, report={self.report})")

        class UserData:
            """
            A class representing a friend or foe user in the report.
            """
            def __init__(self, data: Dict[str, Any]):
                self.name = data.get('name', '')
                self.user_id = data.get('user_id', 0)
                logger.debug(f"Processed UserData: {self}")

            def __repr__(self):
                return f"UserData(name={self.name}, user_id={self.user_id})"

    class Revives:
        def __init__(self, api: TornAPI, user_id: Optional[int]):
            self.api = api
            self.user_id = user_id
            self.revives_data = []
            logger.info("Initialized Revives")

        def fetch_data(self, from_timestamp: Optional[int] = None, 
                                  to_timestamp: Optional[int] = None, 
                                  limit: Optional[int] = None):
            """
            Fetch the latest 100 revives involving faction members.

            Parameters:
            - from_timestamp (int): Limits results to have their timestamp after or on this timestamp.
            - to_timestamp (int): Limits results to have their timestamp before or on this timestamp.
            - limit (int): Limits amount of results. Amount can't be above the default amount.

            Returns:
            - List[ReviveData]: A list of ReviveData instances containing revive details.
            """
            logger.debug(f"Fetching latest revives with params - from: {from_timestamp}, to: {to_timestamp}, limit: {limit}")

            try:
                # Prepare query parameters
                params = {}
                if from_timestamp:
                    params['from'] = from_timestamp
                if to_timestamp:
                    params['to'] = to_timestamp
                if limit:
                    params['limit'] = limit

                # Make API request with user_id specified
                response = self.api.make_request('user', self.user_id,'revives', params)
                logger.debug(f"API response for revives: {response}")

                # Check if the response contains the necessary fields
                if not response or 'revives' not in response:
                    logger.warning("No revives found.")
                    return []

                # Parse and return revives data
                self.revives_data = [self.ReviveData(revive) for revive in response['revives']]
                logger.info(f"Fetched {len(self.revives_data)} revives.")
                return self.revives_data

            except Exception as e:
                logger.error(f"Error fetching revives: {e}")
                return []

        class ReviveData:
            """
            A class representing the details of a revive.
            """
            def __init__(self, data: Dict[str, Any]):
                self.timestamp = data.get('timestamp', 0)
                self.reviver_id = data.get('reviver_id', 0)
                self.reviver_name = data.get('reviver_name', '')
                self.reviver_faction = data.get('reviver_faction', 0)
                self.reviver_factionname = data.get('reviver_factionname', '')
                self.target_id = data.get('target_id', 0)
                self.target_name = data.get('target_name', '')
                self.target_faction = data.get('target_faction', 0)
                self.target_factionname = data.get('target_factionname', '')
                self.target_hospital_reason = data.get('target_hospital_reason', '')
                self.target_last_action = self.LastAction(data.get('target_last_action', {}))
                self.chance = data.get('chance', 0.0)
                self.result = data.get('result', '')
                logger.debug(f"Processed ReviveData: {self}")

            class LastAction:
                """
                A class representing the last action status of the revived target.
                """
                def __init__(self, data: Dict[str, Any]):
                    self.status = data.get('status', '')
                    self.timestamp = data.get('timestamp', 0)
                    logger.debug(f"Processed LastAction: {self}")

            def __repr__(self):
                return (f"ReviveData(timestamp={self.timestamp}, reviver_id={self.reviver_id}, "
                        f"reviver_name={self.reviver_name}, target_id={self.target_id}, "
                        f"target_name={self.target_name}, result={self.result})")

    class RevivesFull:
        def __init__(self, api: TornAPI, user_id: Optional[int]):
            self.api = api
            self.user_id = user_id
            self.revives_data = []
            logger.info("Initialized RevivesFull")

        def fetch_data(self, from_timestamp: Optional[int] = None, 
                                       to_timestamp: Optional[int] = None, 
                                       limit: Optional[int] = None):
            """
            Fetch the latest 1000 revives without names.

            Parameters:
            - from_timestamp (int): Limits results to have their timestamp after or on this timestamp.
            - to_timestamp (int): Limits results to have their timestamp before or on this timestamp.
            - limit (int): Limits amount of results. Amount can't be above the default amount.

            Returns:
            - List[ReviveFullData]: A list of ReviveFullData instances containing revive details.
            """
            logger.debug(f"Fetching latest revives full with params - from: {from_timestamp}, to: {to_timestamp}, limit: {limit}")

            try:
                # Prepare query parameters
                params = {}
                if from_timestamp:
                    params['from'] = from_timestamp
                if to_timestamp:
                    params['to'] = to_timestamp
                if limit:
                    params['limit'] = limit

                # Make API request with user_id specified
                response = self.api.make_request('user', self.user_id, 'revivesfull', params)
                logger.debug(f"API response for revives full: {response}")

                # Check if the response contains the necessary fields
                if not response or 'revives' not in response:
                    logger.warning("No revives found.")
                    return []

                # Parse and return revives full data
                self.revives_data = [self.ReviveFullData(revive) for revive in response['revives']]
                logger.info(f"Fetched {len(self.revives_data)} revives full.")
                return self.revives_data

            except Exception as e:
                logger.error(f"Error fetching revives full: {e}")
                return []

        class ReviveFullData:
            """
            A class representing the details of a revive without player names.
            """
            def __init__(self, data: Dict[str, Any]):
                self.timestamp = data.get('timestamp', 0)
                self.reviver_id = data.get('reviver_id', 0)
                self.reviver_faction = data.get('reviver_faction', 0)
                self.target_id = data.get('target_id', 0)
                self.target_faction = data.get('target_faction', 0)
                self.target_hospital_reason = data.get('target_hospital_reason', '')
                self.target_last_action = self.LastAction(data.get('target_last_action', {}))
                self.chance = data.get('chance', 0.0)
                self.result = data.get('result', '')
                logger.debug(f"Processed ReviveFullData: {self}")

            class LastAction:
                """
                A class representing the last action status of the revived target.
                """
                def __init__(self, data: Dict[str, Any]):
                    self.status = data.get('status', '')
                    self.timestamp = data.get('timestamp', 0)
                    logger.debug(f"Processed LastAction: {self}")

            def __repr__(self):
                return (f"ReviveFullData(timestamp={self.timestamp}, reviver_id={self.reviver_id}, "
                        f"target_id={self.target_id}, result={self.result})")

    class Skills:
        def __init__(self, api: TornAPI, user_id: Optional[int]):
            self.api = api
            self.user_id = user_id
            self.skills_data = None
            logger.info(f"Initialized Skills for User ID: {self.user_id}")

        def fetch_data(self):
            """
            Fetch the skill levels for the user.

            Returns:
            - SkillsData: An instance of SkillsData containing the user's skills.
            """
            logger.debug(f"Fetching skills for User ID: {self.user_id}")
            
            try:
                # Make API request
                response = self.api.make_request('user', self.user_id, 'skills')
                logger.debug(f"API response for skills: {response}")

                # Check if the response contains the necessary fields
                if not response or 'player_id' not in response:
                    logger.warning(f"Skills information not found for User ID: {self.user_id}")
                    return None

                # Parse and return skills data
                self.skills_data = self.SkillsData(response)
                logger.info(f"Fetched skills for User ID: {self.user_id}")
                return self.skills_data

            except Exception as e:
                logger.error(f"Error fetching skills for User ID: {self.user_id}: {e}")
                return None

        class SkillsData:
            """
            A class representing the skill levels of a user.
            """
            def __init__(self, data: Dict[str, Any]):
                try:
                    self.player_id = data.get('player_id')
                    self.bootlegging = data.get('bootlegging', '0')
                    self.burglary = data.get('burglary', '0')
                    self.card_skimming = data.get('card_skimming', '0')
                    self.cracking = data.get('cracking', '0')
                    self.disposal = data.get('disposal', '0')
                    self.forgery = data.get('forgery', '0')
                    self.graffiti = data.get('graffiti', '0')
                    self.hunting = data.get('hunting', '0')
                    self.hustling = data.get('hustling', '0')
                    self.pickpocketing = data.get('pickpocketing', '0')
                    self.racing = data.get('racing', '0')
                    self.reviving = data.get('reviving', '0')
                    self.search_for_cash = data.get('search_for_cash', '0')
                    self.shoplifting = data.get('shoplifting', '0')
                    logger.debug(f"Processed SkillsData: {self}")
                except Exception as e:
                    logger.error(f"Error processing SkillsData: {e}")

            def __repr__(self):
                return (f"SkillsData(player_id={self.player_id}, "
                        f"bootlegging={self.bootlegging}, "
                        f"burglary={self.burglary}, "
                        f"card_skimming={self.card_skimming}, "
                        f"cracking={self.cracking}, "
                        f"disposal={self.disposal}, "
                        f"forgery={self.forgery}, "
                        f"graffiti={self.graffiti}, "
                        f"hunting={self.hunting}, "
                        f"hustling={self.hustling}, "
                        f"pickpocketing={self.pickpocketing}, "
                        f"racing={self.racing}, "
                        f"reviving={self.reviving}, "
                        f"search_for_cash={self.search_for_cash}, "
                        f"shoplifting={self.shoplifting})")

    class Stocks:
        # TODO: neeed testing because of dev having no stock yet 
        def __init__(self, api: TornAPI, user_id: Optional[int]):
            self.api = api
            self.user_id = user_id
            self.stock_data = None
            logger.info(f"Initialized Stocks for User ID: {self.user_id}")

        def fetch_data(self):
            """
            Fetch the stock information for the user.

            Returns:
            - StocksData: An instance of StocksData containing the user's stock information.
            """
            logger.debug(f"Fetching stock information for User ID: {self.user_id}")

            try:
                # Make API request
                response = self.api.make_request('user', self.user_id, 'stocks')
                logger.debug(f"API response for stocks: {response}")

                # Check if the response contains the 'stocks' key
                if not response or 'stocks' not in response:
                    logger.warning(f"No stock information found for User ID: {self.user_id}")
                    return None

                # Handle empty stock list
                if not response['stocks']:
                    logger.info(f"No stocks available for User ID: {self.user_id}")
                    self.stock_data = self.StocksData({})
                    return self.stock_data

                # Parse and return stock data
                self.stock_data = self.StocksData(response['stocks'])
                logger.info(f"Fetched stock information for User ID: {self.user_id}")
                return self.stock_data

            except Exception as e:
                logger.error(f"Error fetching stock information for User ID: {self.user_id}: {e}")
                return None

        class StocksData:
            """
            A class representing the stocks information of a user.
            """
            def __init__(self, data: Dict[str, Any]):
                self.stocks = []

                if data:
                    for stock_id, stock_info in data.items():
                        stock = self.Stock(stock_id, stock_info)
                        self.stocks.append(stock)

                logger.debug(f"Processed StocksData: {self}")

            class Stock:
                """
                A class representing an individual stock.
                """
                def __init__(self, stock_id: int, stock_info: Dict[str, Any]):
                    self.stock_id = stock_id
                    self.benefit = stock_info.get('benefit', {})
                    self.dividend = stock_info.get('dividend', {})
                    self.total_shares = stock_info.get('total_shares', 0)
                    self.transactions = stock_info.get('transactions', {})

                    logger.debug(f"Processed Stock: {self}")

                def __repr__(self):
                    return (f"Stock(stock_id={self.stock_id}, total_shares={self.total_shares}, "
                            f"benefit={self.benefit}, dividend={self.dividend})")

            def __repr__(self):
                return f"StocksData(stocks={self.stocks})"

    class Timestamp:
        def __init__(self, api: TornAPI, user_id: Optional[int]):
            self.api = api
            self.user_id = user_id
            self.current_timestamp = None
            logger.info("Initialized Timestamp API")

        def fetch_data(self):
            """
            Fetch the current timestamp from the TornAPI.

            Returns:
            - int: The current epoch timestamp in seconds.
            """
            logger.debug("Fetching current timestamp")

            try:
                # Make API request
                response = self.api.make_request('user',self.user_id,'timestamp')
                logger.debug(f"API response for timestamp: {response}")

                # Check if the response contains the necessary fields
                if not response or 'timestamp' not in response:
                    logger.warning("Timestamp information not found")
                    return None

                # Store the current timestamp
                self.current_timestamp = response['timestamp']
                logger.info(f"Fetched current timestamp: {self.current_timestamp}")
                return self.current_timestamp

            except Exception as e:
                logger.error(f"Error fetching current timestamp: {e}")
                return None

    class Travel:
        def __init__(self, api: TornAPI, user_id: Optional[int]):
            self.api = api
            self.user_id = user_id
            self.travel_data = None
            logger.info(f"Initialized Travel for User ID: {self.user_id}")

        def fetch_data(self):
            """
            Fetch the travel details for the user.

            Returns:
            - TravelData: An instance of TravelData containing the user's travel information.
            """
            logger.debug(f"Fetching travel information for User ID: {self.user_id}")

            try:
                # Make API request
                response = self.api.make_request('user', self.user_id, 'travel')
                logger.debug(f"API response for travel information: {response}")

                # Check if the response contains the necessary fields
                if not response or 'travel' not in response:
                    logger.warning(f"Travel information not found for User ID: {self.user_id}")
                    return None

                # Parse and return travel data
                self.travel_data = self.TravelData(response['travel'])
                logger.info(f"Fetched travel information for User ID: {self.user_id}")
                return self.travel_data

            except Exception as e:
                logger.error(f"Error fetching travel information for User ID: {self.user_id}: {e}")
                return None

        class TravelData:
            """
            A class representing the travel information of a user.
            """
            def __init__(self, data: Dict[str, Any]):
                try:
                    self.departed = data.get('departed', None)
                    self.destination = data.get('destination', None)
                    self.method = data.get('method', None)
                    self.time_left = data.get('time_left', None)
                    self.timestamp = data.get('timestamp', None)
                    logger.debug(f"Processed TravelData: {self}")
                except Exception as e:
                    logger.error(f"Error processing TravelData: {e}")

            def __repr__(self):
                return (f"TravelData(departed={self.departed}, "
                        f"destination={self.destination}, "
                        f"method={self.method}, "
                        f"time_left={self.time_left}, "
                        f"timestamp={self.timestamp})")

    class WeaponExp:
        # TODO: Needs to be tested 
        def __init__(self, api: TornAPI, user_id: Optional[int] = None):
            self.api = api
            self.user_id = user_id
            self.weapon_exp_data = None
            logger.info(f"Initialized WeaponExp for User ID: {self.user_id}")

        def fetch_data(self):
            """
            Fetch the weapon experience for the user.

            Returns:
            - WeaponExpData: An instance of WeaponExpData containing the user's weapon experience.
            """
            logger.debug(f"Fetching weapon experience for User ID: {self.user_id}")

            try:
                # Make API request
                response = self.api.make_request('user', self.user_id, 'weaponexp')
                logger.debug(f"API response for weapon experience: {response}")

                # Check if the response contains the 'weaponexp' key
                if not response or 'weaponexp' not in response:
                    logger.warning(f"Weapon experience information not found for User ID: {self.user_id}")
                    return None

                # Parse and return weapon experience data
                self.weapon_exp_data = self.WeaponExpData(response['weaponexp'])
                logger.info(f"Fetched weapon experience for User ID: {self.user_id}")
                return self.weapon_exp_data

            except Exception as e:
                logger.error(f"Error fetching weapon experience for User ID: {self.user_id}: {e}")
                return None

        class WeaponExpData:
            """
            A class representing the weapon experience of a user.
            """
            def __init__(self, data: Dict[str, Any]):
                self.weapon_experiences = []

                if data:
                    for item in data:
                        weapon_exp = self.WeaponExperience(item)
                        self.weapon_experiences.append(weapon_exp)

                logger.debug(f"Processed WeaponExpData: {self}")

            class WeaponExperience:
                """
                A class representing individual weapon experience.
                """
                def __init__(self, data: Dict[str, Any]):
                    self.exp = data.get('exp', 0)
                    self.itemID = data.get('itemID', 0)
                    self.name = data.get('name', '')

                    logger.debug(f"Processed WeaponExperience: {self}")

                def __repr__(self):
                    return (f"WeaponExperience(itemID={self.itemID}, exp={self.exp}, "
                            f"name={self.name})")

            def __repr__(self):
                return f"WeaponExpData(weapon_experiences={self.weapon_experiences})"
    
    class WorkStats:
        def __init__(self, api: TornAPI, user_id: Optional[int]):
            self.api = api
            self.user_id = user_id
            self.work_stats_data = None
            logger.info(f"Initialized WorkStats for User ID: {self.user_id}")

        def fetch_data(self):
            """
            Fetch the work stats for the user.

            Returns:
            - WorkStatsData: An instance of WorkStatsData containing the user's work stats.
            """
            logger.debug(f"Fetching work stats for User ID: {self.user_id}")

            # Check if user_id is valid
            if self.user_id is None:
                logger.warning("User ID is not set.")
                return None

            try:
                # Make API request
                response = self.api.make_request('user', self.user_id, 'workstats')
                logger.debug(f"API response for work stats: {response}")

                # Check if the response contains the necessary fields
                if not response or 'endurance' not in response:
                    logger.warning(f"Work stats information not found for User ID: {self.user_id}")
                    return None

                # Parse and return work stats data
                self.work_stats_data = self.WorkStatsData(response)
                logger.info(f"Fetched work stats for User ID: {self.user_id}")
                return self.work_stats_data

            except Exception as e:
                logger.error(f"Error fetching work stats for User ID: {self.user_id}: {e}")
                return None

        class WorkStatsData:
            def __init__(self, data: Dict[str, Any]):
                self.endurance = data.get('endurance', 0)
                self.intelligence = data.get('intelligence', 0)
                self.manual_labor = data.get('manual_labor', 0)
                logger.debug(f"Processed WorkStatsData: {self}")

            def __repr__(self):
                return (f"WorkStatsData(endurance={self.endurance}, "
                        f"intelligence={self.intelligence}, "
                        f"manual_labor={self.manual_labor})")
