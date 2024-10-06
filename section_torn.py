from typing import Dict, Any, Optional, List
from tornApi import TornAPI
from env_loader import load_environment_variables
from logger import setup_logger, close_logger
from enum import Enum
from datetime import datetime

env = load_environment_variables()
if env is None:
    raise ValueError("Failed to load environment variables.")
logger, file_handler = setup_logger('Sections', env['DEBUG_LEVEL'])

class Torn:
    
    def __init__(self, api: TornAPI, id: Optional[int] = None):
        """
        Initialize the Torn class with the TornAPI.

        Args:
        - api: An instance of the TornAPI class.
        - id: Optional; The default ID to use for API requests.
        """
        self.api = api
        self.id = id   
        self.bank = self.Bank(self.api)
        self.cards = self.Cards(self.api)
        self.chainreport = self.ChainReport(self.api, self.id)
        self.cityshops = self.CityShops(self.api)
        self.companies = self.Companies(self.api, self.id)
        self.competition = self.Competition(self.api)
        self.education = self.Education(self.api, self.id)
        self.factiontree = self.FactionTree(self.api)
        self.gyms = self.Gyms(self.api, self.id)
        self.honors = self.Honors(self.api, self.id)
        self.itemdetails = self.ItemDetails(self.api, self.id)
        self.items = self.Items(self.api, self.id)
        self.itemstats = self.ItemStats(self.api, self.id)
        # Initialize other sections here...

        logger.info("Initialized Torn class")

    class Bank:
        def __init__(self, api: TornAPI):
            self.api = api
            self.data = None
            logger.info("Initialized Bank for Torn section")

        def fetch_data(self):
            """
            Fetch data for the Bank using TornAPI.

            Returns:
            - BankData: An instance of BankData containing the fetched data.
            """
            logger.debug("Fetching bank data")

            try:
                response = self.api.make_request('torn', '', 'bank')
                logger.debug(f"API response for bank: {response}")

                if not response or 'bank' not in response:
                    logger.warning("Bank data not found in the response")
                    return None

                self.data = self.BankData(response['bank'])
                logger.info("Fetched bank data successfully")
                return self.data

            except Exception as e:
                logger.error(f"Error fetching bank data: {e}")
                return None

        class BankData:
            def __init__(self, data: Dict[str, Any]):
                """
                Parse and store the bank data.

                Args:
                - data: A dictionary containing the fetched bank data.
                """
                self.one_month = float(data.get('1m', 0))
                self.one_week = float(data.get('1w', 0))
                self.two_months = float(data.get('2m', 0))
                self.two_weeks = float(data.get('2w', 0))
                self.three_months = float(data.get('3m', 0))

                logger.debug(f"Processed BankData: {self}")

            def __repr__(self):
                return (f"BankData(1m={self.one_month}, 1w={self.one_week}, "
                        f"2m={self.two_months}, 2w={self.two_weeks}, "
                        f"3m={self.three_months})")

    class Cards:
        def __init__(self, api: TornAPI):
            self.api = api
            self.data = None
            logger.info("Initialized Cards for Torn section")

        def fetch_data(self):
            """
            Fetch data for the Cards using TornAPI.

            Returns:
            - CardsData: An instance of CardsData containing the fetched data.
            """
            logger.debug("Fetching cards data")

            try:
                response = self.api.make_request('torn', '', 'cards')
                logger.debug(f"API response for cards: {response}")

                if not response or 'cards' not in response:
                    logger.warning("Cards data not found in the response")
                    return None

                self.data = self.CardsData(response['cards'])
                logger.info("Fetched cards data successfully")
                return self.data

            except Exception as e:
                logger.error(f"Error fetching cards data: {e}")
                return None

        class CardsData:
            def __init__(self, data: Dict[str, Any]):
                """
                Parse and store the cards data.

                Args:
                - data: A dictionary containing the fetched cards data.
                """
                self.cards = {card_id: self.Card(card_data) for card_id, card_data in data.items()}
                logger.debug(f"Processed CardsData: {len(self.cards)} cards")

            def __repr__(self):
                return f"CardsData(cards_count={len(self.cards)})"

            def __getitem__(self, card_id):
                return self.cards.get(card_id)

            class Card:
                def __init__(self, data: Dict[str, Any]):
                    self.cost = data.get('cost', 0)
                    self.description = data.get('description', '')
                    self.name = data.get('name', '')
                    self.rarity = data.get('rarity', '')
                    self.type = data.get('type', '')

                def __repr__(self):
                    return f"Card(name={self.name}, rarity={self.rarity})"
#TODO: Check if chainreport is correct
    class ChainReport:
        def __init__(self, api: TornAPI, id: Optional[int] = None):
            self.api = api
            self.id = id
            self.data = None
            logger.info("Initialized ChainReport for Torn section")

        def fetch_data(self, chain_id: Optional[int] = None):
            """
            Fetch data for the Chain Report using TornAPI.

            Args:
            - chain_id: Optional; The ID of the chain to fetch the report for. If not provided, uses the default ID.

            Returns:
            - ChainReportData: An instance of ChainReportData containing the fetched data, or None if no data is available.
            """
            id_to_use = chain_id if chain_id is not None else self.id
            logger.debug(f"Fetching chain report data for chain ID: {id_to_use}")

            try:
                response = self.api.make_request('torn', id_to_use, 'chainreport')
                logger.debug(f"API response for chain report: {response}")

                if isinstance(response, dict) and 'chainreport' in response:
                    if 'code' in response['chainreport'] and response['chainreport']['code'] == 6:
                        logger.info("No chain report data available")
                        return None
                    else:
                        self.data = self.ChainReportData(response['chainreport'])
                        logger.info("Fetched chain report data successfully")
                        return self.data
                else:
                    logger.warning("Unexpected response format for chain report")
                    return None

            except Exception as e:
                logger.error(f"Error fetching chain report data: {e}")
                return None

        class ChainReportData:
            def __init__(self, data: Dict[str, Any]):
                self.assists = data.get('assists', 0)
                self.besthit = data.get('besthit', 0)
                self.bonuses = [self.BonusHit(bonus) for bonus in data.get('bonuses', [])]
                self.chain = data.get('chain', 0)
                self.code = data.get('code', 0)
                self.draws = data.get('draws', 0)
                self.end = datetime.fromtimestamp(data.get('end', 0))
                self.error = data.get('error', '')
                self.escapes = data.get('escapes', 0)
                self.faction_id = data.get('factionID', 0)
                self.hospitalize = data.get('hospitalize', 0)
                self.leave = data.get('leave', 0)
                self.losses = data.get('losses', 0)
                self.members = self.Members(data.get('members', {}))
                self.mug = data.get('mug', 0)
                self.overseas = data.get('overseas', 0)
                self.respect = data.get('respect', 0.0)
                self.retaliations = data.get('retaliations', 0)
                self.start = datetime.fromtimestamp(data.get('start', 0))
                self.targets = data.get('targets', 0)
                self.warhits = data.get('warhits', 0)

            def __repr__(self):
                return f"ChainReportData(chain={self.chain}, respect={self.respect}, members_count={len(self.members)})"

            class BonusHit:
                def __init__(self, data: Dict[str, Any]):
                    self.attacker = data.get('attacker', 0)
                    self.chain = data.get('chain', 0)
                    self.defender = data.get('defender', 0)
                    self.respect = data.get('respect', 0.0)

                def __repr__(self):
                    return f"BonusHit(attacker={self.attacker}, defender={self.defender}, respect={self.respect})"

            class Members:
                def __init__(self, data: Dict[str, Any]):
                    self.members = {int(user_id): self.Member(member_data) for user_id, member_data in data.items()}

                def __getitem__(self, user_id: int):
                    return self.members.get(user_id)

                def __len__(self):
                    return len(self.members)

                def __repr__(self):
                    return f"Members(count={len(self.members)})"

                class Member:
                    def __init__(self, data: Dict[str, Any]):
                        self.assist = data.get('assist', 0)
                        self.attacks = data.get('attacks', 0)
                        self.avg = data.get('avg', 0.0)
                        self.best = data.get('best', 0.0)
                        self.bonus = data.get('bonus', 0)
                        self.draw = data.get('draw', 0)
                        self.escape = data.get('escape', 0)
                        self.faction_id = data.get('factionID', 0)
                        self.hosp = data.get('hosp', 0)
                        self.leave = data.get('leave', 0)
                        self.level = data.get('level', 0)
                        self.loss = data.get('loss', 0)
                        self.mug = data.get('mug', 0)
                        self.overseas = data.get('overseas', 0)
                        self.respect = data.get('respect', 0.0)
                        self.retal = data.get('retal', 0)
                        self.user_id = data.get('userID', 0)
                        self.war = data.get('war', 0)

                    def __repr__(self):
                        return f"Member(user_id={self.user_id}, respect={self.respect})"

    class CityShops:
        def __init__(self, api: TornAPI):
            self.api = api
            self.data = None
            logger.info("Initialized CityShops for Torn section")

        def fetch_data(self):
            """
            Fetch data for the CityShops using TornAPI.

            Returns:
            - CityShopsData: An instance of CityShopsData containing the fetched data.
            """
            logger.debug("Fetching city shops data")

            try:
                response = self.api.make_request('torn', '', 'cityshops')
                logger.debug(f"API response for city shops: {response}")

                if not response or 'cityshops' not in response:
                    logger.warning("City shops data not found in the response")
                    return None

                self.data = self.CityShopsData(response['cityshops'])
                logger.info("Fetched city shops data successfully")
                return self.data

            except Exception as e:
                logger.error(f"Error fetching city shops data: {e}")
                return None

        class CityShopsData:
            def __init__(self, data: Dict[str, Any]):
                """
                Parse and store the city shops data.

                Args:
                - data: A dictionary containing the fetched city shops data.
                """
                self.shops = {shop_id: self.Shop(shop_data) for shop_id, shop_data in data.items()}
                logger.debug(f"Processed CityShopsData: {len(self.shops)} shops")

            def __repr__(self):
                return f"CityShopsData(shops_count={len(self.shops)})"

            def __getitem__(self, shop_id):
                return self.shops.get(shop_id)

            class Shop:
                def __init__(self, data: Dict[str, Any]):
                    self.name = data.get('name', '')
                    self.inventory = self.Inventory(data.get('inventory', {}))

                def __repr__(self):
                    return f"Shop(name={self.name}, inventory_count={len(self.inventory.items)})"

                class Inventory:
                    def __init__(self, data: Dict[str, Any]):
                        self.items = {item_id: self.Item(item_data) for item_id, item_data in data.items()}

                    def __repr__(self):
                        return f"Inventory(items_count={len(self.items)})"

                    def __getitem__(self, item_id):
                        return self.items.get(item_id)

                    class Item:
                        def __init__(self, data: Dict[str, Any]):
                            self.in_stock = data.get('in_stock', 0)
                            self.name = data.get('name', '')
                            self.price = data.get('price', 0)
                            self.type = data.get('type', '')

                        def __repr__(self):
                            return f"Item(name={self.name}, in_stock={self.in_stock}, price={self.price})"

    class Companies:
        def __init__(self, api: TornAPI, id: Optional[int] = None):
            self.api = api
            self.id = id
            self.data = None
            logger.info("Initialized Companies for Torn section")

        def fetch_data(self, company_id: Optional[int] = None):
            """
            Fetch data for the Companies using TornAPI.

            Args:
            - company_id: Optional; The ID of a specific company to fetch data for. If not provided, uses the default ID.

            Returns:
            - CompaniesData: An instance of CompaniesData containing the fetched data.
            """
            id_to_use = company_id if company_id is not None else self.id
            logger.debug(f"Fetching companies data{'for company ID: ' + str(id_to_use) if id_to_use else ''}")

            try:
                response = self.api.make_request('torn', id_to_use, 'companies')
                logger.debug(f"API response for companies: {response}")

                if not response or 'companies' not in response:
                    logger.warning("Companies data not found in the response")
                    return None

                self.data = self.CompaniesData(response['companies'], id_to_use)
                logger.info("Fetched companies data successfully")
                return self.data

            except Exception as e:
                logger.error(f"Error fetching companies data: {e}")
                return None

        class CompaniesData:
            def __init__(self, data: Dict[str, Any], id: Optional[int] = None):
                """
                Parse and store the companies data.

                Args:
                - data: A dictionary containing the fetched companies data.
                - id: Optional; The ID of a specific company if provided.
                """
                self.companies = {company_id: self.Company(company_data) for company_id, company_data in data.items()}
                self.id = id
                logger.debug(f"Processed CompaniesData: {len(self.companies)} companies")

            def __repr__(self):
                return f"CompaniesData(companies_count={len(self.companies)})"

            def __getitem__(self, company_id):
                if isinstance(company_id, int):
                    return self.companies.get(str(company_id))
                return self.companies.get(company_id)

            def __iter__(self):
                return iter(self.companies.values())

            @property
            def company(self):
                if self.id is not None:
                    return self.companies.get(str(self.id))
                return None

            class Company:
                def __init__(self, data: Dict[str, Any]):
                    self.cost = data.get('cost', 0)
                    self.default_employees = data.get('default_employees', 0)
                    self.name = data.get('name', '')
                    self.positions = self.Positions(data.get('positions', {}))
                    self.specials = self.Specials(data.get('specials', {}))
                    self.stock = self.Stocks(data.get('stock', {}))

                def __repr__(self):
                    return f"Company(name={self.name}, positions={len(self.positions.positions)})"

                class Positions:
                    def __init__(self, data: Dict[str, Any]):
                        self.positions = {name: self.Position(position_data) for name, position_data in data.items()}

                    def __repr__(self):
                        return f"Positions(count={len(self.positions)})"

                    def __getitem__(self, name):
                        return self.positions.get(name)

                    class Position:
                        class SpecialAbility(Enum):
                            CLEANER = "Cleaner"
                            MANAGER = "Manager"
                            MARKETER = "Marketer"
                            NONE = "None"
                            SECRETARY = "Secretary"
                            TRAINER = "Trainer"

                        def __init__(self, data: Dict[str, Any]):
                            self.description = data.get('description', '')
                            self.end_gain = data.get('end_gain', 0)
                            self.end_required = data.get('end_required', 0)
                            self.int_gain = data.get('int_gain', 0)
                            self.int_required = data.get('int_required', 0)
                            self.man_gain = data.get('man_gain', 0)
                            self.man_required = data.get('man_required', 0)
                            self.special_ability = self.SpecialAbility(data.get('special_ability', 'None'))

                        def __repr__(self):
                            return f"Position(special_ability={self.special_ability.value})"

                class Specials:
                    def __init__(self, data: Dict[str, Any]):
                        self.specials = {name: self.Special(special_data) for name, special_data in data.items()}

                    def __repr__(self):
                        return f"Specials(count={len(self.specials)})"

                    def __getitem__(self, name):
                        return self.specials.get(name)

                    class Special:
                        def __init__(self, data: Dict[str, Any]):
                            self.cost = data.get('cost', 0)
                            self.effect = data.get('effect', '')
                            self.rating_required = data.get('rating_required', 0)

                        def __repr__(self):
                            return f"Special(effect={self.effect})"

                class Stocks:
                    def __init__(self, data: Dict[str, Any]):
                        self.stocks = {name: self.Stock(stock_data) for name, stock_data in data.items()}

                    def __repr__(self):
                        return f"Stocks(count={len(self.stocks)})"

                    def __getitem__(self, name):
                        return self.stocks.get(name)

                    class Stock:
                        def __init__(self, data: Dict[str, Any]):
                            self.cost = data.get('cost', 0)

    class Competition:
        #TODO : handle the error when the competition is not found
        def __init__(self, api: TornAPI):
            self.api = api
            self.data = None
            logger.info("Initialized Competition for Torn section")

        def fetch_data(self):
            """
            Fetch data for the Competition using TornAPI.

            Returns:
            - CompetitionData: An instance of CompetitionData containing the fetched data.
            """
            logger.debug("Fetching competition data")

            try:
                response = self.api.make_request('torn', '', 'competition')
                logger.debug(f"API response for competition: {response}")

                if not response or 'competition' not in response:
                    logger.warning("Competition data not found in the response")
                    return None

                self.data = self.CompetitionData(response['competition'])
                logger.info("Fetched competition data successfully")
                return self.data

            except Exception as e:
                logger.error(f"Error fetching competition data: {e}")
                return None

        class CompetitionData:
            class CompetitionType(Enum):
                DOG_TAGS = "Dog Tags"
                EASTER_EGG_HUNT = "Easter Egg Hunt"
                ELIMINATION = "Elimination"
                HALLOWEEN = "Halloween"
                MR_AND_MS_TORN = "Mr & Ms Torn"

            class EliminationStatus(Enum):
                UNKNOWN = "<unknown>"
                BEFORE_ELIMINATED = "before-eliminated"
                ELIMINATED = "eliminated"

            def __init__(self, data: Dict[str, Any]):
                self.leaderboard_mr = [self.LeaderboardPosition(pos) for pos in data.get('leaderboardmr', [])]
                self.leaderboard_mrs = [self.LeaderboardPosition(pos) for pos in data.get('leaderboardmrs', [])]
                self.name = self.CompetitionType(data.get('name', ''))
                self.teams = [self.EliminationTeam(team) for team in data.get('teams', [])]

            def __repr__(self):
                return f"CompetitionData(name={self.name.value}, teams_count={len(self.teams)})"

            class LeaderboardPosition:
                def __init__(self, data: Dict[str, Any]):
                    self.position = data.get('position', 0)
                    self.score = float(data.get('score', 0))
                    self.user_id = data.get('user_id', 0)

                def __repr__(self):
                    return f"LeaderboardPosition(position={self.position}, user_id={self.user_id}, score={self.score})"

            class EliminationTeam:
                def __init__(self, data: Dict[str, Any]):
                    self.lives = data.get('lives', 0)
                    self.losses = data.get('losses', 0)
                    self.name = data.get('name', '')
                    self.participants = data.get('participants', None)  # Unknown structure
                    self.position = data.get('position', 0)
                    self.score = data.get('score', 0)
                    self.status = Torn.Competition.CompetitionData.EliminationStatus(data.get('status', '<unknown>'))
                    self.team = data.get('team', '')
                    self.wins = data.get('wins', 0)

                def __repr__(self):
                    return f"EliminationTeam(name={self.name}, position={self.position}, status={self.status.value})"

    class Education:
        def __init__(self, api: TornAPI, id: Optional[int] = None):
            self.api = api
            self.id = id
            self.data = None
            logger.info("Initialized Education for Torn section")

        def fetch_data(self, education_id: Optional[int] = None):
            """
            Fetch data for the Education using TornAPI.

            Args:
            - education_id: Optional; The ID of a specific education to fetch data for. If not provided, uses the default ID.

            Returns:
            - EducationsData: An instance of EducationsData containing the fetched data.
            """
            id_to_use = education_id if education_id is not None else self.id
            logger.debug(f"Fetching education data{'for education ID: ' + str(id_to_use) if id_to_use else ''}")

            try:
                response = self.api.make_request('torn', id_to_use, 'education')
                logger.debug(f"API response for education: {response}")

                if not response or 'education' not in response:
                    logger.warning("Education data not found in the response")
                    return None

                self.data = self.EducationsData(response['education'])
                logger.info("Fetched education data successfully")
                return self.data

            except Exception as e:
                logger.error(f"Error fetching education data: {e}")
                return None

        class EducationsData:
            def __init__(self, data: Dict[str, Any]):
                self.educations = {edu_id: self.Education(edu_data) for edu_id, edu_data in data.items()}

            def __repr__(self):
                return f"EducationsData(educations_count={len(self.educations)})"

            def __getitem__(self, edu_id):
                return self.educations.get(edu_id)

            class Education:
                def __init__(self, data: Dict[str, Any]):
                    self.code = data.get('code', '')
                    self.description = data.get('description', '')
                    self.duration = data.get('duration', 0)
                    self.money_cost = data.get('money_cost', 0)
                    self.name = data.get('name', '')
                    self.prerequisites = data.get('prerequisites', [])
                    self.results = self.Results(data.get('results', {}))
                    self.tier = data.get('tier', 0)

                def __repr__(self):
                    return f"Education(name={self.name}, tier={self.tier})"

                class Results:
                    def __init__(self, data: Dict[str, Any]):
                        self.endurance = data.get('endurance', [])
                        self.intelligence = data.get('intelligence', [])
                        self.manual_labor = data.get('manual_labor', [])
                        self.perk = data.get('perk', [])

                    def __repr__(self):
                        return f"Results(endurance={len(self.endurance)}, intelligence={len(self.intelligence)}, manual_labor={len(self.manual_labor)}, perk={len(self.perk)})"

    class FactionTree:
        def __init__(self, api: TornAPI):
            self.api = api
            self.data = None
            logger.info("Initialized FactionTree for Torn section")

        def fetch_data(self):
            """
            Fetch data for the FactionTree using TornAPI.

            Returns:
            - FactionTreeData: An instance of FactionTreeData containing the fetched data.
            """
            logger.debug("Fetching faction tree data")

            try:
                response = self.api.make_request('torn', '', 'factiontree')
                logger.debug(f"API response for faction tree: {response}")

                if not response or 'factiontree' not in response:
                    logger.warning("Faction tree data not found in the response")
                    return None

                self.data = self.FactionTreeData(response['factiontree'])
                logger.info("Fetched faction tree data successfully")
                return self.data

            except Exception as e:
                logger.error(f"Error fetching faction tree data: {e}")
                return None

        class FactionTreeData:
            class Branch(Enum):
                AGGRESSION = "Aggression"
                CORE = "Core"
                CRIMINALITY = "Criminality"
                EXCURSION = "Excursion"
                FORTITUDE = "Fortitude"
                STEADFAST = "Steadfast"
                SUPPRESSION = "Suppression"
                TOLERATION = "Toleration"
                VORACITY = "Voracity"

            def __init__(self, data: Dict[str, Any]):
                self.branches = {branch_id: self.BranchTree(branch_data) for branch_id, branch_data in data.items()}

            def __repr__(self):
                return f"FactionTreeData(branches_count={len(self.branches)})"

            class BranchTree:
                def __init__(self, data: Dict[str, Any]):
                    self.levels = {level: self.Level(level_data) for level, level_data in data.items()}

                def __repr__(self):
                    return f"BranchTree(levels_count={len(self.levels)})"

                class Level:
                    def __init__(self, data: Dict[str, Any]):
                        self.ability = data.get('ability', '')
                        self.base_cost = data.get('base_cost', 0)
                        self.branch = Torn.FactionTree.FactionTreeData.Branch(data.get('branch', ''))
                        self.challenge = data.get('challenge', '')
                        self.name = data.get('name', '')

                    def __repr__(self):
                        return f"Level(name={self.name}, branch={self.branch.value})"

    class Gyms:
        def __init__(self, api: TornAPI, id: Optional[int] = None):
            self.api = api
            self.id = id
            self.data = None
            logger.info("Initialized Gyms for Torn section")

        def fetch_data(self, gym_id: Optional[int] = None):
            """
            Fetch data for the Gyms using TornAPI.

            Args:
            - gym_id: Optional; The ID of a specific gym to fetch data for. If not provided, uses the default ID.

            Returns:
            - GymsData: An instance of GymsData containing the fetched data.
            """
            id_to_use = gym_id if gym_id is not None else self.id
            logger.debug(f"Fetching gyms data{'for gym ID: ' + str(id_to_use) if id_to_use else ''}")

            try:
                response = self.api.make_request('torn', id_to_use, 'gyms')
                logger.debug(f"API response for gyms: {response}")

                if not response or 'gyms' not in response:
                    logger.warning("Gyms data not found in the response")
                    return None

                self.data = self.GymsData(response['gyms'])
                logger.info("Fetched gyms data successfully")
                return self.data

            except Exception as e:
                logger.error(f"Error fetching gyms data: {e}")
                return None

        class GymsData:
            def __init__(self, data: Dict[str, Any]):
                self.gyms = {gym_id: self.Gym(gym_data) for gym_id, gym_data in data.items()}

            def __repr__(self):
                return f"GymsData(gyms_count={len(self.gyms)})"

            def __getitem__(self, gym_id):
                return self.gyms.get(gym_id)

            class Gym:
                def __init__(self, data: Dict[str, Any]):
                    self.cost = data.get('cost', 0)
                    self.defense = data.get('defense', 0)
                    self.dexterity = data.get('dexterity', 0)
                    self.energy = data.get('energy', 0)
                    self.name = data.get('name', '')
                    self.note = data.get('note', '')
                    self.speed = data.get('speed', 0)
                    self.stage = data.get('stage', 0)
                    self.strength = data.get('strength', 0)

                def __repr__(self):
                    return f"Gym(name={self.name}, stage={self.stage})"

    class Honors:
        def __init__(self, api: TornAPI, id: Optional[int] = None):
            self.api = api
            self.id = id
            self.data = None
            logger.info("Initialized Honors for Torn section")

        def fetch_data(self, honor_id: Optional[int] = None):
            """
            Fetch data for the Honors using TornAPI.

            Args:
            - honor_id: Optional; The ID of a specific honor to fetch data for. If not provided, uses the default ID.

            Returns:
            - HonorsData: An instance of HonorsData containing the fetched data.
            """
            id_to_use = honor_id if honor_id is not None else self.id
            logger.debug(f"Fetching honors data{' for honor ID: ' + str(id_to_use) if id_to_use else ''}")

            try:
                response = self.api.make_request('torn', id_to_use, 'honors')
                logger.debug(f"API response for honors: {response}")

                if not response or 'honors' not in response:
                    logger.warning("Honors data not found in the response")
                    return None

                self.data = self.HonorsData(response['honors'])
                logger.info("Fetched honors data successfully")
                return self.data

            except Exception as e:
                logger.error(f"Error fetching honors data: {e}")
                return None

        class HonorsData:
            class Rarity(Enum):
                COMMON = "Common"
                EXTREMELY_RARE = "Extremely Rare"
                LIMITED = "Limited"
                RARE = "Rare"
                UNCOMMON = "Uncommon"
                VERY_COMMON = "Very Common"
                VERY_RARE = "Very Rare"
                NULL = "Null"  # Add NULL option

            def __init__(self, data: Dict[str, Any]):
                if isinstance(data, dict):
                    self.honors = {honor_id: self.Honor(honor_data) for honor_id, honor_data in data.items()}
                else:
                    logger.error("Invalid data format for honors")
                    self.honors = {}

            def __repr__(self):
                return f"HonorsData(honors_count={len(self.honors)})"

            def __getitem__(self, honor_id):
                return self.honors.get(honor_id)

            class Honor:
                def __init__(self, data: Dict[str, Any]):
                    self.circulation = data.get('circulation', 0)
                    self.description = data.get('description', '')
                    self.equipped = data.get('equipped', '')
                    self.name = data.get('name', '')
                    
                    # Corrected rarity handling
                    rarity_value = data.get('rarity', '')
                    try:
                        # Use the value to match against the enum
                        self.rarity = Torn.Honors.HonorsData.Rarity(rarity_value)
                    except ValueError:
                        logger.info(f"Invalid rarity value '{rarity_value}' for honor '{self.name}', defaulting to 'Null'")
                        self.rarity = Torn.Honors.HonorsData.Rarity.NULL
                    
                    self.type = data.get('type', 0)

                def __repr__(self):
                    return f"Honor(name={self.name}, rarity={self.rarity.value})"

    class ItemDetails:
        def __init__(self, api: TornAPI, id: Optional[int] = None):
            self.api = api
            self.id = id
            self.data = None
            logger.info("Initialized ItemDetails for Torn section")

        def fetch_data(self, item_id: Optional[int] = None):
            """
            Fetch data for the ItemDetails using TornAPI.

            Args:
            - item_id: Optional; The ID of the item to fetch details for. If not provided, uses the ID set during initialization.

            Returns:
            - ItemData: An instance of ItemData containing the fetched data.
            """
            
            logger.info("Fetching item details data for item ID: %s", self.id)
            id_to_use = item_id if item_id is not None else self.id
            logger.info("Item ID to use: %s", id_to_use)
            if id_to_use is None:
                logger.error("No item ID provided for fetching item details")
                return None

            logger.debug(f"Fetching item details data for item ID: {id_to_use}")

            try:
                response = self.api.make_request('torn', id_to_use, 'itemdetails')
                logger.debug(f"API response for item details: {response}")

                if not response or 'itemdetails' not in response:
                    logger.warning("Item details data not found in the response")
                    return None

                self.data = self.ItemData(response['itemdetails'])
                logger.info("Fetched item details data successfully")
                return self.data

            except Exception as e:
                logger.error(f"Error fetching item details data: {e}")
                return None

        class ItemData:
            class Rarity(Enum):
                NONE = "None"
                ORANGE = "Orange"
                RED = "Red"
                YELLOW = "Yellow"

            def __init__(self, data: Dict[str, Any]):
                self.accuracy = float(data.get('accuracy', 0))
                self.armor = float(data.get('armor', 0))
                self.bonuses = self.Bonuses(data.get('bonuses', {}))
                self.damage = float(data.get('damage', 0))
                self.ID = data.get('ID', 0)
                self.name = data.get('name', '')
                self.quality = float(data.get('quality', 0))
                self.rarity = self.Rarity(data.get('rarity', 'None'))
                self.type = data.get('type', '')
                self.UID = data.get('UID', 0)

            def __repr__(self):
                return f"ItemData(name={self.name}, rarity={self.rarity.value})"

            class Bonuses:
                def __init__(self, data: Dict[str, Any]):
                    self.bonuses = {bonus_id: self.Bonus(bonus_data) for bonus_id, bonus_data in data.items()}

                def __repr__(self):
                    return f"Bonuses(count={len(self.bonuses)})"

                def __getitem__(self, bonus_id):
                    return self.bonuses.get(bonus_id)

                class Bonus:
                    def __init__(self, data: Dict[str, Any]):
                        self.bonus = data.get('bonus', '')
                        self.description = data.get('description', '')
                        self.value = data.get('value', 0)

                    def __repr__(self):
                        return f"Bonus(bonus={self.bonus}, value={self.value})"

    class Items:
        def __init__(self, api: TornAPI, id: Optional[int] = None):
            self.api = api
            self.id = id
            self.data = None
            logger.info("Initialized Items for Torn section")

        def fetch_data(self, item_id: Optional[int] = None):
            """
            Fetch data for the Items using TornAPI.

            Args:
            - item_id: Optional; The ID of a specific item to fetch data for. If not provided, uses the default ID.

            Returns:
            - ItemsData: An instance of ItemsData containing the fetched data.
            """
            id_to_use = item_id if item_id is not None else self.id
            logger.debug(f"Fetching items data{' for item ID: ' + str(id_to_use) if id_to_use else ''}")

            try:
                response = self.api.make_request('torn', id_to_use, 'items')
                logger.debug(f"API response for items: {response}")

                if not response or 'items' not in response:
                    logger.warning("Items data not found in the response")
                    return None

                self.data = self.ItemsData(response['items'])
                logger.info("Fetched items data successfully")
                return self.data

            except Exception as e:
                logger.error(f"Error fetching items data: {e}")
                return None

        class ItemsData:
            def __init__(self, data: Dict[str, Any]):
                self.items = {item_id: self.Item(item_data) for item_id, item_data in data.items()}
                logger.debug(f"Processed ItemsData: {len(self.items)} items")

            def __repr__(self):
                return f"ItemsData(items_count={len(self.items)})"

            def __getitem__(self, item_id):
                return self.items.get(item_id)

            class Item:
                def __init__(self, data: Dict[str, Any]):
                    self.buy_price = data.get('buy_price', 0)
                    self.circulation = data.get('circulation', 0)
                    self.coverage = self.Coverage(data.get('coverage', {}))
                    self.description = data.get('description', '')
                    self.effect = data.get('effect', '')
                    self.image = data.get('image', '')
                    self.market_value = data.get('market_value', 0)
                    self.name = data.get('name', '')
                    self.requirement = data.get('requirement', '')
                    self.sell_price = data.get('sell_price', 0)
                    self.type = data.get('type', '')
                    self.weapon_type = data.get('weapon_type', '')

                def __repr__(self):
                    return f"Item(name={self.name}, type={self.type})"

                class Coverage:
                    def __init__(self, data: Dict[str, Any]):
                        self.arm_coverage = data.get('Arm Coverage', 0.0)
                        self.chest_coverage = data.get('Chest Coverage', 0.0)
                        self.foot_coverage = data.get('Foot Coverage', 0.0)
                        self.full_body_coverage = data.get('Full Body Coverage', 0.0)
                        self.groin_coverage = data.get('Groin Coverage', 0.0)
                        self.hand_coverage = data.get('Hand Coverage', 0.0)
                        self.head_coverage = data.get('Head Coverage', 0.0)
                        self.heart_coverage = data.get('Heart Coverage', 0.0)
                        self.leg_coverage = data.get('Leg Coverage', 0.0)
                        self.stomach_coverage = data.get('Stomach Coverage', 0.0)
                        self.throat_coverage = data.get('Throat Coverage', 0.0)

    class ItemStats:
        def __init__(self, api: TornAPI, id: Optional[int] = None):
            self.api = api
            self.id = id
            self.data = None
            logger.info("Initialized ItemStats for Torn section")

        def fetch_data(self, item_id: Optional[int] = None):
            """
            Fetch data for the ItemStats using TornAPI.

            Args:
            - item_id: Optional; The ID of the item to fetch stats for. If not provided, uses the ID set during initialization.

            Returns:
            - ItemStatsData: An instance of ItemStatsData containing the fetched data.
            """
            id_to_use = item_id if item_id is not None else self.id
            logger.debug(f"Fetching item stats data for item ID: {id_to_use}")

            if id_to_use is None:
                logger.error("No item ID provided for fetching item stats")
                return None

            try:
                response = self.api.make_request('torn', id_to_use, 'itemstats')
                logger.debug(f"API response for item stats: {response}")

                if not response or 'itemstats' not in response:
                    logger.warning("Item stats data not found in the response")
                    return None

                self.data = self.ItemStatsData(response['itemstats'])
                logger.info("Fetched item stats data successfully")
                return self.data

            except Exception as e:
                logger.error(f"Error fetching item stats data: {e}")
                return None

        class ItemStatsData:
            def __init__(self, data: Dict[str, Any]):
                self.ID = data.get('ID', 0)
                self.market_price = data.get('market_price', 0)
                self.name = data.get('name', '')
                self.stats = self.Stats(data.get('stats', {}))
                self.type = data.get('type', '')
                self.UID = data.get('UID', 0)

            def __repr__(self):
                return f"ItemStatsData(name={self.name}, type={self.type})"

            class Stats:
                def __init__(self, data: Dict[str, Any]):
                    self.critical_hits = data.get('critical_hits', 0)
                    self.damage = data.get('damage', 0)
                    self.damage_mitigated = float(data.get('damage_mitigated', 0.0))
                    self.damage_taken = float(data.get('damage_taken', 0.0))
                    self.finishing_hits = data.get('finishing_hits', 0)
                    self.first_faction_owner = data.get('first_faction_owner', 0)
                    self.first_owner = data.get('first_owner', 0)
                    self.highest_damage = data.get('highest_damage', 0)
                    self.hits = data.get('hits', 0)
                    self.hits_received = float(data.get('hits_received', 0.0))
                    self.misses = data.get('misses', 0)
                    self.most_damage_mitigated = float(data.get('most_damage_mitigated', 0.0))
                    self.most_damage_taken = float(data.get('most_damage_taken', 0.0))
                    self.reloads = data.get('reloads', 0)
                    self.respect_earned = float(data.get('respect_earned', 0.0))
                    self.rounds_fired = data.get('rounds_fired', 0)
                    self.time_created = datetime.fromtimestamp(data.get('time_created', 0))

                def __repr__(self):
                    return (f"Stats(damage={self.damage}, critical_hits={self.critical_hits}, "
                            f"respect_earned={self.respect_earned})")