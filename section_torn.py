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
        self.logcategories = self.LogCategories(self.api)
        self.logtypes = self.LogTypes(self.api)
        self.lookup = self.Lookup(self.api) 
        self.medals = self.Medals(self.api)
        self.organisedcrimes = self.OrganisedCrimes(self.api, self.id)
        self.pawnshop = self.Pawnshop(self.api)
        self.properties = self.Properties(self.api)
        self.rackets = self.Rackets(self.api)
        self.raids = self.Raids(self.api)
        self.rankedwars = self.RankedWars(self.api)
        self.rankedwarreport = self.RankedWarReport(self.api, self.id)
        self.stats = self.Stats(self.api)
        self.stocks = self.Stocks(self.api, self.id)
        self.territory = self.Territory(self.api)
        self.territorynames = self.TerritoryNames(self.api)
        self.territorywarreport = self.TerritoryWarReport(self.api, self.id)
        self.territorywars = self.TerritoryWars(self.api)
        self.timestamp = self.Timestamp()

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

    class LogCategories:
        def __init__(self, api: TornAPI):
            self.api = api
            self.data = None
            logger.info("Initialized LogCategories for Torn section")

        def fetch_data(self):
            """
            Fetch data for the LogCategories using TornAPI.

            Returns:
            - LogCategoriesData: An instance of LogCategoriesData containing the fetched data.
            """
            logger.debug("Fetching log categories data")

            try:
                response = self.api.make_request('torn', '', 'logcategories')
                logger.debug(f"API response for log categories: {response}")

                if not response or 'logcategories' not in response:
                    logger.warning("Log categories data not found in the response")
                    return None

                self.data = self.LogCategoriesData(response['logcategories'])
                logger.info("Fetched log categories data successfully")
                return self.data

            except Exception as e:
                logger.error(f"Error fetching log categories data: {e}")
                return None

        class LogCategoriesData:
            def __init__(self, data: Dict[str, Any]):
                self.categories = {category_id: category_name for category_id, category_name in data.items() }
                logger.debug(f"Processed LogCategoriesData: {len(self.categories)} categories")

            def __repr__(self):
                return f"LogCategoriesData(categories_count={len(self.categories)})"

            def __getitem__(self, category_id):
                return self.categories.get(category_id)

    class LogTypes:
        def __init__(self, api: TornAPI):
            self.api = api
            self.data = None
            logger.info("Initialized LogTypes for Torn section")

        def fetch_data(self):
            """
            Fetch data for the LogTypes using TornAPI.

            Returns:
            - LogTypesData: An instance of LogTypesData containing the fetched data.
            """
            logger.debug("Fetching log types data")

            try:
                response = self.api.make_request('torn', '', 'logtypes')
                logger.debug(f"API response for log types: {response}")

                if not response or 'logtypes' not in response:
                    logger.warning("Log types data not found in the response")
                    return None

                self.data = self.LogTypesData(response['logtypes'])
                logger.info("Fetched log types data successfully")
                return self.data

            except Exception as e:
                logger.error(f"Error fetching log types data: {e}")
                return None

        class LogTypesData:
            def __init__(self, data: Dict[str, Any]):
                self.types = {type_id: type_name for type_id, type_name in data.items()}
                logger.debug(f"Processed LogTypesData: {len(self.types)} types")

            def __repr__(self):
                return f"LogTypesData(types_count={len(self.types)})"

            def __getitem__(self, type_id):
                return self.types.get(type_id)

    class Lookup:
        def __init__(self, api: TornAPI):
            self.api = api
            self.data = None
            logger.info("Initialized Lookup for Torn section")

        def fetch_data(self, section: str):
            """
            Fetch data for the Lookup using TornAPI.

            Args:
            - section: The section to look up selections for.

            Returns:
            - LookupData: An instance of LookupData containing the fetched data.
            """
            logger.debug(f"Fetching lookup data for section: {section}")

            try:
                response = self.api.make_request('torn', '', 'lookup', selections=section)
                logger.debug(f"API response for lookup: {response}")

                if not response or 'selections' not in response:
                    logger.warning("Lookup data not found in the response")
                    return None

                self.data = self.LookupData(response['selections'])
                logger.info(f"Fetched lookup data successfully for section: {section}")
                return self.data

            except Exception as e:
                logger.error(f"Error fetching lookup data: {e}")
                return None

        class LookupData:
            def __init__(self, data: List[str]):
                self.selections = data
                logger.debug(f"Processed LookupData: {len(self.selections)} selections")

            def __repr__(self):
                return f"LookupData(selections_count={len(self.selections)})"

            def __iter__(self):
                return iter(self.selections)

            def __getitem__(self, index):
                return self.selections[index]            
                        
    class Medals:
        def __init__(self, api: TornAPI, id: Optional[int] = None):
            self.api = api
            self.id = id
            self.data = None
            logger.info("Initialized Medals for Torn section")

        def fetch_data(self, medal_id: Optional[int] = None):
            """
            Fetch data for the Medals using TornAPI.

            Args:
            - medal_id: Optional; The ID of a specific medal to fetch data for. If not provided, uses the default ID.

            Returns:
            - MedalsData: An instance of MedalsData containing the fetched data.
            """
            id_to_use = medal_id if medal_id is not None else self.id
            logger.debug(f"Fetching medals data{'for medal ID: ' + str(id_to_use) if id_to_use else ''}")

            try:
                response = self.api.make_request('torn', id_to_use, 'medals')
                logger.debug(f"API response for medals: {response}")

                if not response or 'medals' not in response:
                    logger.warning("Medals data not found in the response")
                    return None

                self.data = self.MedalsData(response['medals'])
                logger.info("Fetched medals data successfully")
                return self.data

            except Exception as e:
                logger.error(f"Error fetching medals data: {e}")
                return None

        class MedalsData:
            def __init__(self, data: Dict[str, Any]):
                """
                Parse and store the medals data.

                Args:
                - data: A dictionary containing the fetched medals data.
                """
                self.medals = {medal_id: self.Medal(medal_data) for medal_id, medal_data in data.items()}
                logger.debug(f"Processed MedalsData: {len(self.medals)} medals")

            def __repr__(self):
                return f"MedalsData(medals_count={len(self.medals)})"

            def __getitem__(self, medal_id):
                return self.medals.get(medal_id)

            class Medal:
                class Rarity(Enum):
                    UNKNOWN = "Unknown Rarity"
                    VERY_COMMON = "Very Common"
                    COMMON = "Common"
                    UNCOMMON = "Uncommon"
                    RARE = "Rare"
                    VERY_RARE = "Very Rare"
                    EXTREMELY_RARE = "Extremely Rare"
                    LIMITED = "Limited"

                def __init__(self, data: Dict[str, Any]):
                    self.circulation = data.get('circulation', 0)
                    self.description = data.get('description', '')
                    self.equipped = data.get('equipped', '')
                    self.name = data.get('name', '')
                    self.type = data.get('type', '')
                    self.rarity = self.determine_rarity(data.get('rarity'), self.circulation)

                def determine_rarity(self, rarity_str: Optional[str], circulation: int) -> Rarity:
                    """
                    Determine the rarity of the medal based on the rarity string and circulation.
                    If rarity is not provided or unknown, estimate it based on circulation.
                    """

                    try:
                        return self.Rarity(rarity_str)
                    except ValueError:
                        logger.info(f"Unrecognized rarity '{rarity_str}' for medal '{self.name}'. Estimating based on circulation.")

                def __repr__(self):
                    return f"Medal(name={self.name}, rarity={self.rarity.value}, circulation={self.circulation})"
            
    class OrganisedCrimes:
        def __init__(self, api: TornAPI, id: Optional[int] = None):
            self.api = api
            self.id = id
            self.data = None
            logger.info("Initialized OrganisedCrimes for Torn section")

        def fetch_data(self):
            """
            Fetch data for the OrganisedCrimes using TornAPI.

            Returns:
            - OrganisedCrimesData: An instance of OrganisedCrimesData containing the fetched data.
            """
            logger.debug("Fetching organised crimes data")

            try:
                response = self.api.make_request('torn', self.id, 'organisedcrimes')
                logger.debug(f"API response for organised crimes: {response}")

                if not response or 'organisedcrimes' not in response:
                    logger.warning("Organised crimes data not found in the response")
                    return None

                self.data = self.OrganisedCrimesData(response['organisedcrimes'])
                logger.info("Fetched organised crimes data successfully")
                return self.data

            except Exception as e:
                logger.error(f"Error fetching organised crimes data: {e}")
                return None

        class OrganisedCrimesData:
            def __init__(self, data: Dict[str, Any]):
                """
                Parse and store the organised crimes data.

                Args:
                - data: A dictionary containing the fetched organised crimes data.
                """
                self.crimes = {crime_id: self.OrganisedCrime(crime_data) for crime_id, crime_data in data.items()}
                logger.debug(f"Processed OrganisedCrimesData: {len(self.crimes)} crimes")

            def __repr__(self):
                return f"OrganisedCrimesData(crimes_count={len(self.crimes)})"

            def __getitem__(self, crime_id):
                return self.crimes.get(crime_id)

            class OrganisedCrime:
                def __init__(self, data: Dict[str, Any]):
                    self.max_cash = data.get('max_cash', 0)
                    self.max_respect = data.get('max_respect', 0)
                    self.members = data.get('members', 0)
                    self.min_cash = data.get('min_cash', 0)
                    self.min_respect = data.get('min_respect', 0)
                    self.name = data.get('name', '')
                    self.time = data.get('time', 0)

                def __repr__(self):
                    return f"OrganisedCrime(name={self.name}, members={self.members}, time={self.time})"
    
    class Pawnshop:
        def __init__(self, api: TornAPI):
            self.api = api
            self.data = None
            logger.info("Initialized Pawnshop for Torn section")

        def fetch_data(self):
            """
            Fetch data for the Pawnshop using TornAPI.

            Returns:
            - PawnshopData: An instance of PawnshopData containing the fetched data.
            """
            logger.debug("Fetching pawnshop data")

            try:
                response = self.api.make_request('torn', '', 'pawnshop')
                logger.debug(f"API response for pawnshop: {response}")

                if not response or 'pawnshop' not in response:
                    logger.warning("Pawnshop data not found in the response")
                    return None

                self.data = self.PawnshopData(response['pawnshop'])
                logger.info("Fetched pawnshop data successfully")
                return self.data

            except Exception as e:
                logger.error(f"Error fetching pawnshop data: {e}")
                return None

        class PawnshopData:
            def __init__(self, data: Dict[str, Any]):
                """
                Parse and store the pawnshop data.

                Args:
                - data: A dictionary containing the fetched pawnshop data.
                """
                self.donatorpack_value = data.get('donatorpack_value', 0)
                self.points_value = data.get('points_value', 0)
                logger.debug(f"Processed PawnshopData: donatorpack_value={self.donatorpack_value}, points_value={self.points_value}")

            def __repr__(self):
                return f"PawnshopData(donatorpack_value={self.donatorpack_value}, points_value={self.points_value})"

    class PokerTables:
        def __init__(self, api: TornAPI):
            self.api = api
            self.data = None
            logger.info("Initialized PokerTables for Torn section")

        def fetch_data(self):
            """
            Fetch data for the PokerTables using TornAPI.

            Returns:
            - Dict[str, PokerTableData]: A dictionary of PokerTableData instances, keyed by table ID.
            """
            logger.debug("Fetching poker tables data")

            try:
                response = self.api.make_request('torn', '', 'pokertables')
                logger.debug(f"API response for poker tables: {response}")

                if not response or 'pokertables' not in response:
                    logger.warning("Poker tables data not found in the response")
                    return None

                self.data = {table_id: self.PokerTableData(table_data) for table_id, table_data in response['pokertables'].items()}
                logger.info("Fetched poker tables data successfully")
                return self.data

            except Exception as e:
                logger.error(f"Error fetching poker tables data: {e}")
                return None

        class PokerTableData:
            def __init__(self, data: Dict[str, Any]):
                """
                Parse and store the poker table data.

                Args:
                - data: A dictionary containing the fetched poker table data.
                """
                self.big_blind = data.get('big_blind', 0)
                self.current_players = data.get('current_players', 0)
                self.maximum_players = data.get('maximum_players', 0)
                self.name = data.get('name', '')
                self.small_blind = data.get('small_blind', 0)
                self.speed = data.get('speed', 0)
                logger.debug(f"Processed PokerTableData: {self}")

            def __repr__(self):
                return f"PokerTableData(name='{self.name}', current_players={self.current_players}, maximum_players={self.maximum_players}, small_blind={self.small_blind}, big_blind={self.big_blind}, speed={self.speed})"
   
    class Properties:
        def __init__(self, api: TornAPI, id: Optional[int] = None):
            self.api = api
            self.id = id
            self.data = None
            logger.info("Initialized Properties for Torn section")

        def fetch_data(self):
            """
            Fetch data for the Properties using TornAPI.

            Returns:
            - Dict[str, PropertyData]: A dictionary of PropertyData instances, keyed by property ID.
            """
            logger.debug("Fetching properties data")

            try:
                response = self.api.make_request('torn', self.id, 'properties')
                logger.debug(f"API response for properties: {response}")

                if not response or 'properties' not in response:
                    logger.warning("Properties data not found in the response")
                    return None

                self.data = {prop_id: self.PropertyData(prop_data) for prop_id, prop_data in response['properties'].items()}
                logger.info("Fetched properties data successfully")
                return self.data

            except Exception as e:
                logger.error(f"Error fetching properties data: {e}")
                return None

        class PropertyData:
            def __init__(self, data: Dict[str, Any]):
                """
                Parse and store the property data.

                Args:
                - data: A dictionary containing the fetched property data.
                """
                self.cost = data.get('cost', '')
                self.happy = data.get('happy', 0)
                self.name = data.get('name', '')
                self.staff_available = data.get('staff_available', [])
                self.upgrades_available = data.get('upgrades_available', [])
                logger.debug(f"Processed PropertyData: {self}")

            def __repr__(self):
                return f"PropertyData(name='{self.name}', cost='{self.cost}', happy={self.happy}, staff_available={self.staff_available}, upgrades_available={self.upgrades_available})"

    class Rackets:
        def __init__(self, api: TornAPI):
            self.api = api
            self.data = None
            logger.info("Initialized Rackets for Torn section")

        def fetch_data(self):
            """
            Fetch data for the Rackets using TornAPI.

            Returns:
            - Dict[str, RacketData]: A dictionary of RacketData instances, keyed by territory.
            """
            logger.debug("Fetching rackets data")

            try:
                response = self.api.make_request('torn', '', 'rackets')
                logger.debug(f"API response for rackets: {response}")

                if not response or 'rackets' not in response:
                    logger.warning("Rackets data not found in the response")
                    return None

                self.data = {territory: self.RacketData(racket_data) for territory, racket_data in response['rackets'].items()}
                logger.info("Fetched rackets data successfully")
                return self.data

            except Exception as e:
                logger.error(f"Error fetching rackets data: {e}")
                return None

        class RacketData:
            def __init__(self, data: Dict[str, Any]):
                """
                Parse and store the racket data.

                Args:
                - data: A dictionary containing the fetched racket data.
                """
                self.changed = data.get('changed', 0)
                self.created = data.get('created', 0)
                self.faction = data.get('faction', 0)
                self.level = data.get('level', 0)
                self.name = data.get('name', '')
                self.reward = data.get('reward', '')
                logger.debug(f"Processed RacketData: {self}")

            def __repr__(self):
                return f"RacketData(name='{self.name}', faction={self.faction}, level={self.level}, reward='{self.reward}', changed={self.changed}, created={self.created})"

    class RaidReport:
        def __init__(self, api: TornAPI, id: Optional[int] = None):
            self.api = api
            self.id = id
            self.data = None
            logger.info(f"Initialized RaidReport for Torn section with ID: {self.id}")

        def fetch_data(self):
            """
            Fetch data for the Raid Report using TornAPI.

            Returns:
            - RaidReportData: An instance of RaidReportData containing the fetched data.
            """
            if self.id is None:
                logger.error("Raid report ID is required but not provided")
                return None

            logger.debug(f"Fetching raid report data for ID: {self.id}")

            try:
                response = self.api.make_request('torn', self.id, 'raidreport')
                logger.debug(f"API response for raid report: {response}")

                if not response or 'raidreport' not in response:
                    logger.warning("Raid report data not found in the response")
                    return None

                self.data = self.RaidReportData(response['raidreport'])
                logger.info(f"Fetched raid report data successfully for ID: {self.id}")
                return self.data

            except Exception as e:
                logger.error(f"Error fetching raid report data: {e}")
                return None

        class RaidReportData:
            def __init__(self, data: Dict[str, Any]):
                """
                Parse and store the raid report data.

                Args:
                - data: A dictionary containing the fetched raid report data.
                """
                self.factions = self.Factions(data.get('factions', {}))
                self.war = self.RaidWar(data.get('war', {}))
                logger.debug(f"Processed RaidReportData: {self}")

            def __repr__(self):
                return f"RaidReportData(factions={self.factions}, war={self.war})"

            class Factions:
                def __init__(self, data: Dict[str, Any]):
                    self.factions = {faction_id: self.Faction(faction_data) for faction_id, faction_data in data.items()}

                def __repr__(self):
                    return f"Factions({len(self.factions)} factions)"

                class Faction:
                    def __init__(self, data: Dict[str, Any]):
                        self.attacks = data.get('attacks', 0)
                        self.members = self.Members(data.get('members', {}))
                        self.name = data.get('name', '')
                        self.score = data.get('score', 0)
                        self.type = data.get('type', '')

                    def __repr__(self):
                        return f"Faction(name='{self.name}', attacks={self.attacks}, score={self.score}, type='{self.type}')"

                    class Members:
                        def __init__(self, data: Dict[str, Any]):
                            self.members = {user_id: self.User(user_data) for user_id, user_data in data.items()}

                        def __repr__(self):
                            return f"Members({len(self.members)} members)"

                        class User:
                            def __init__(self, data: Dict[str, Any]):
                                self.attacks = data.get('attacks', 0)
                                self.damage = data.get('damage', 0.0)
                                self.faction_id = data.get('faction_id', 0)
                                self.level = data.get('level', 0)
                                self.name = data.get('name', '')

                            def __repr__(self):
                                return f"User(name='{self.name}', attacks={self.attacks}, damage={self.damage}, level={self.level})"

            class RaidWar:
                def __init__(self, data: Dict[str, Any]):
                    self.end = data.get('end', 0)
                    self.start = data.get('start', 0)

                def __repr__(self):
                    return f"RaidWar(start={self.start}, end={self.end})"

    class Raids:
        def __init__(self, api: TornAPI):
            self.api = api
            self.data = None
            logger.info("Initialized Raids for Torn section")

        def fetch_data(self):
            """
            Fetch data for ongoing raids using TornAPI.

            Returns:
            - RaidsData: An instance of RaidsData containing the fetched data.
            """
            logger.debug("Fetching raids data")

            try:
                response = self.api.make_request('torn', '', 'raids')
                logger.debug(f"API response for raids: {response}")

                if not response or 'raids' not in response:
                    logger.warning("Raids data not found in the response")
                    return None

                self.data = self.RaidsData(response['raids'])
                logger.info("Fetched raids data successfully")
                return self.data

            except Exception as e:
                logger.error(f"Error fetching raids data: {e}")
                return None

        class RaidsData:
            def __init__(self, data: Dict[str, Any]):
                """
                Parse and store the raids data.

                Args:
                - data: A dictionary containing the fetched raids data.
                """
                self.raids = {raid_id: self.Raid(raid_data) for raid_id, raid_data in data.items()}
                logger.debug(f"Processed RaidsData: {len(self.raids)} raids")

            def __repr__(self):
                return f"RaidsData(raids_count={len(self.raids)})"

            def __getitem__(self, raid_id):
                return self.raids.get(raid_id)

            class Raid:
                def __init__(self, data: Dict[str, Any]):
                    self.assaulting_faction = data.get('assaulting_faction', 0)
                    self.assaulting_score = data.get('assaulting_score', 0.0)
                    self.defending_faction = data.get('defending_faction', 0)
                    self.defending_score = data.get('defending_score', 0.0)
                    self.started = data.get('started', 0)

                def __repr__(self):
                    return f"Raid(assaulting_faction={self.assaulting_faction}, defending_faction={self.defending_faction}, started={self.started})"
  
    class RankedWarReport:
        def __init__(self, api: TornAPI, id: int):
            self.api = api
            self.id = id
            self.data = None
            logger.info(f"Initialized RankedWarReport for Torn section with ID: {self.id}")

        def fetch_data(self):
            """
            Fetch data for the Ranked War Report using TornAPI.

            Returns:
            - RankedWarReportData: An instance of RankedWarReportData containing the fetched data.
            """
            if self.id is None:
                logger.error("Ranked war report ID is required but not provided")
                return None

            logger.debug(f"Fetching ranked war report data for ID: {self.id}")

            try:
                response = self.api.make_request('torn', self.id, 'rankedwarreport')
                logger.debug(f"API response for ranked war report: {response}")

                if not response or 'rankedwarreport' not in response:
                    logger.warning("Ranked war report data not found in the response")
                    return None

                self.data = self.RankedWarReportData(response['rankedwarreport'])
                logger.info(f"Fetched ranked war report data successfully for ID: {self.id}")
                return self.data

            except Exception as e:
                logger.error(f"Error fetching ranked war report data: {e}")
                return None

        class RankedWarReportData:
            def __init__(self, data: Dict[str, Any]):
                """
                Parse and store the ranked war report data.

                Args:
                - data: A dictionary containing the fetched ranked war report data.
                """
                self.factions = {faction_id: self.Faction(faction_data) for faction_id, faction_data in data.get('factions', {}).items()}
                self.war = self.War(data.get('war', {}))
                logger.debug(f"Processed RankedWarReportData: {self}")

            def __repr__(self):
                return f"RankedWarReportData(factions={self.factions}, war={self.war})"

            class Faction:
                def __init__(self, data: Dict[str, Any]):
                    self.attacks = data.get('attacks', 0)
                    self.members = {user_id: self.User(user_data) for user_id, user_data in data.get('members', {}).items()}
                    self.name = data.get('name', '')
                    self.rank_after = data.get('rank_after', '')
                    self.rank_before = data.get('rank_before', '')
                    self.rewards = self.Rewards(data.get('rewards', {}))
                    self.score = data.get('score', 0)
                    logger.debug(f"Processed Faction: {self}")

                def __repr__(self):
                    return f"Faction(name='{self.name}', score={self.score})"

                class User:
                    def __init__(self, data: Dict[str, Any]):
                        self.attacks = data.get('attacks', 0)
                        self.faction_id = data.get('faction_id', 0)
                        self.level = data.get('level', 0)
                        self.name = data.get('name', '')
                        self.score = data.get('score', 0.0)
                        logger.debug(f"Processed User: {self}")

                    def __repr__(self):
                        return f"User(name='{self.name}', score={self.score})"

                class Rewards:
                    def __init__(self, data: Dict[str, Any]):
                        self.items = {item_id: self.Item(item_data) for item_id, item_data in data.get('items', {}).items()}
                        self.points = data.get('points', 0)
                        self.respect = data.get('respect', 0)
                        logger.debug(f"Processed Rewards: {self}")

                    def __repr__(self):
                        return f"Rewards(points={self.points}, respect={self.respect})"

                    class Item:
                        def __init__(self, data: Dict[str, Any]):
                            self.name = data.get('name', '')
                            self.quantity = data.get('quantity', 0)
                            logger.debug(f"Processed Item: {self}")

                        def __repr__(self):
                            return f"Item(name='{self.name}', quantity={self.quantity})"

            class War:
                def __init__(self, data: Dict[str, Any]):
                    self.end = data.get('end', 0)
                    self.forfeit = data.get('forfeit', 0)
                    self.start = data.get('start', 0)
                    self.winner = data.get('winner', 0)
                    logger.debug(f"Processed War: {self}")

                def __repr__(self):
                    return f"War(start={self.start}, end={self.end}, winner={self.winner})"

    class RankedWars:
        def __init__(self, api: TornAPI):
            self.api = api
            self.data = None
            logger.info("Initialized RankedWars for Torn section")

        def fetch_data(self):
            """
            Fetch data for the RankedWars using TornAPI.

            Returns:
            - Dict[str, RankedWar]: A dictionary of RankedWar instances, keyed by war ID.
            """
            logger.debug("Fetching ranked wars data")

            try:
                response = self.api.make_request('torn', '', 'rankedwars')
                logger.debug(f"API response for ranked wars: {response}")

                if not response or 'rankedwars' not in response:
                    logger.warning("Ranked wars data not found in the response")
                    return None

                self.data = {war_id: self.RankedWar(war_data) for war_id, war_data in response['rankedwars'].items()}
                logger.info("Fetched ranked wars data successfully")
                return self.data

            except Exception as e:
                logger.error(f"Error fetching ranked wars data: {e}")
                return None

        class RankedWar:
            def __init__(self, data: Dict[str, Any]):
                self.factions = {faction_id: self.Faction(faction_data) for faction_id, faction_data in data.get('factions', {}).items()}
                self.war = self.War(data.get('war', {}))
                logger.debug(f"Processed RankedWar: {self}")

            def __repr__(self):
                return f"RankedWar(factions={list(self.factions.keys())}, war={self.war})"

            class Faction:
                def __init__(self, data: Dict[str, Any]):
                    self.chain = data.get('chain', 0)
                    self.name = data.get('name', '')
                    self.score = data.get('score', 0)
                    logger.debug(f"Processed Faction: {self}")

                def __repr__(self):
                    return f"Faction(name='{self.name}', score={self.score}, chain={self.chain})"

            class War:
                def __init__(self, data: Dict[str, Any]):
                    self.end = data.get('end', 0)
                    self.start = data.get('start', 0)
                    self.target = data.get('target', 0)
                    self.winner = data.get('winner', 0)
                    logger.debug(f"Processed War: {self}")

                def __repr__(self):
                    return f"War(start={self.start}, end={self.end}, target={self.target}, winner={self.winner})"
    
    class RockPaperScissors:
        def __init__(self, api: TornAPI):
            self.api = api
            self.data = None
            logger.info("Initialized RockPaperScissors for Torn section")

        def fetch_data(self):
            """
            Fetch data for the RockPaperScissors using TornAPI.

            Returns:
            - List[RockPaperScissorsData]: A list of RockPaperScissorsData instances.
            """
            logger.debug("Fetching rock paper scissors data")

            try:
                response = self.api.make_request('torn', '', 'rockpaperscissors')
                logger.debug(f"API response for rock paper scissors: {response}")

                if not response or 'rockpaperscissors' not in response:
                    logger.warning("Rock paper scissors data not found in the response")
                    return None

                self.data = [self.RockPaperScissorsData(rps_data) for rps_data in response['rockpaperscissors']]
                logger.info("Fetched rock paper scissors data successfully")
                return self.data

            except Exception as e:
                logger.error(f"Error fetching rock paper scissors data: {e}")
                return None

        class RockPaperScissorsData:
            def __init__(self, data: Dict[str, Any]):
                """
                Parse and store the rock paper scissors data.

                Args:
                - data: A dictionary containing the fetched rock paper scissors data.
                """
                self.count = data.get('count', 0)
                self.type = data.get('type', '')
                logger.debug(f"Processed RockPaperScissorsData: {self}")

            def __repr__(self):
                return f"RockPaperScissorsData(count={self.count}, type='{self.type}')"
    
    class SearchForCash:
        def __init__(self, api: TornAPI):
            self.api = api
            self.data = None
            logger.info("Initialized SearchForCash for Torn section")

        def fetch_data(self):
            """
            Fetch data for the SearchForCash using TornAPI.

            Returns:
            - Dict[str, SearchForCashSubcrimeData]: A dictionary of SearchForCashSubcrimeData instances, keyed by subcrime name.
            """
            logger.debug("Fetching search for cash data")

            try:
                response = self.api.make_request('torn', '', 'searchforcash')
                logger.debug(f"API response for search for cash: {response}")

                if not response or 'searchforcash' not in response:
                    logger.warning("Search for cash data not found in the response")
                    return None

                self.data = {subcrime_name: self.SearchForCashSubcrimeData(subcrime_data) for subcrime_name, subcrime_data in response['searchforcash'].items()}
                logger.info("Fetched search for cash data successfully")
                return self.data

            except Exception as e:
                logger.error(f"Error fetching search for cash data: {e}")
                return None

        class SearchForCashSubcrimeData:
            def __init__(self, data: Dict[str, Any]):
                """
                Parse and store the search for cash subcrime data.

                Args:
                - data: A dictionary containing the fetched search for cash subcrime data.
                """
                self.percentage = data.get('percentage', 0.0)
                self.title = data.get('title', '')
                logger.debug(f"Processed SearchForCashSubcrimeData: {self}")

            def __repr__(self):
                return f"SearchForCashSubcrimeData(percentage={self.percentage}, title='{self.title}')"
    
    class Stats:
        def __init__(self, api: TornAPI):
            self.api = api
            self.data = None
            logger.info("Initialized Stats for Torn section")

        def fetch_data(self, timestamp: Optional[int] = None):
            """
            Fetch data for the Stats using TornAPI.

            Args:
            - timestamp: Optional; Specify which date (in epoch seconds) to get the stats from.

            Returns:
            - StatsData: An instance of StatsData containing the fetched data.
            """
            logger.debug("Fetching stats data")

            params = {}
            if timestamp:
                params['timestamp'] = timestamp

            try:
                response = self.api.make_request('torn', '', 'stats', params=params)
                logger.debug(f"API response for stats: {response}")

                if not response or 'stats' not in response:
                    logger.warning("Stats data not found in the response")
                    return None

                self.data = self.StatsData(response['stats'])
                logger.info("Fetched stats data successfully")
                return self.data

            except Exception as e:
                logger.error(f"Error fetching stats data: {e}")
                return None

        class StatsData:
            def __init__(self, data: Dict[str, Any]):
                """
                Parse and store the stats data.

                Args:
                - data: A dictionary containing the fetched stats data.
                """
                self.communication_articlereads = data.get('communication_articlereads', 0)
                self.communication_articles = data.get('communication_articles', 0)
                self.communication_articleviews = data.get('communication_articleviews', 0)
                self.communication_chats = data.get('communication_chats', 0)
                self.communication_events = data.get('communication_events', 0)
                self.communication_forumposts = data.get('communication_forumposts', 0)
                self.communication_messages = data.get('communication_messages', 0)
                self.communication_totalevents = data.get('communication_totalevents', 0)
                self.communication_totalmessages = data.get('communication_totalmessages', 0)
                self.crimes = data.get('crimes', 0)
                self.crimes_today = data.get('crimes_today', 0)
                self.events = data.get('events', 0)
                self.forums_dislikes = data.get('forums_dislikes', 0)
                self.forums_likes = data.get('forums_likes', 0)
                self.forums_posts = data.get('forums_posts', 0)
                self.forums_threads = data.get('forums_threads', 0)
                self.gym_trains = data.get('gym_trains', 0)
                self.items = data.get('items', 0)
                self.jailed = data.get('jailed', 0)
                self.job_army = data.get('job_army', 0)
                self.job_casino = data.get('job_casino', 0)
                self.job_company = data.get('job_company', 0)
                self.job_education = data.get('job_education', 0)
                self.job_grocer = data.get('job_grocer', 0)
                self.job_law = data.get('job_law', 0)
                self.job_medical = data.get('job_medical', 0)
                self.job_none = data.get('job_none', 0)
                self.money_citybank = data.get('money_citybank', 0)
                self.money_onhand = data.get('money_onhand', 0)
                self.points_averagecost = data.get('points_averagecost', 0)
                self.points_bought = data.get('points_bought', 0)
                self.points_market = data.get('points_market', 0)
                self.points_total = data.get('points_total', 0)
                self.timestamp = data.get('timestamp', 0)
                self.total_attacks_criticalhits = data.get('total_attacks_criticalhits', 0)
                self.total_attacks_hits = data.get('total_attacks_hits', 0)
                self.total_attacks_lost = data.get('total_attacks_lost', 0)
                self.total_attacks_misses = data.get('total_attacks_misses', 0)
                self.total_attacks_moneymugged = data.get('total_attacks_moneymugged', 0)
                self.total_attacks_respectgained = data.get('total_attacks_respectgained', 0)
                self.total_attacks_roundsfired = data.get('total_attacks_roundsfired', 0)
                self.total_attacks_runaway = data.get('total_attacks_runaway', 0)
                self.total_attacks_stalemated = data.get('total_attacks_stalemated', 0)
                self.total_attacks_stealthed = data.get('total_attacks_stealthed', 0)
                self.total_attacks_won = data.get('total_attacks_won', 0)
                self.total_bounty_placed = data.get('total_bounty_placed', 0)
                self.total_bounty_rewards = data.get('total_bounty_rewards', 0)
                self.total_classifiedads_placed = data.get('total_classifiedads_placed', 0)
                self.total_company_trains = data.get('total_company_trains', 0)
                self.total_drugs_cannabis = data.get('total_drugs_cannabis', 0)
                self.total_drugs_ecstacy = data.get('total_drugs_ecstacy', 0)
                self.total_drugs_ketamine = data.get('total_drugs_ketamine', 0)
                self.total_drugs_lsd = data.get('total_drugs_lsd', 0)
                self.total_drugs_opium = data.get('total_drugs_opium', 0)
                self.total_drugs_overdosed = data.get('total_drugs_overdosed', 0)
                self.total_drugs_pcp = data.get('total_drugs_pcp', 0)
                self.total_drugs_shrooms = data.get('total_drugs_shrooms', 0)
                self.total_drugs_speed = data.get('total_drugs_speed', 0)
                self.total_drugs_used = data.get('total_drugs_used', 0)
                self.total_drugs_vicodin = data.get('total_drugs_vicodin', 0)
                self.total_drugs_xanax = data.get('total_drugs_xanax', 0)
                self.total_hospital_medicalitemsused = data.get('total_hospital_medicalitemsused', 0)
                self.total_hospital_revived = data.get('total_hospital_revived', 0)
                self.total_hospital_trips = data.get('total_hospital_trips', 0)
                self.total_items_auctionswon = data.get('total_items_auctionswon', 0)
                self.total_items_bazaarbought = data.get('total_items_bazaarbought', 0)
                self.total_items_bazaarincome = data.get('total_items_bazaarincome', 0)
                self.total_items_cityfinds = data.get('total_items_cityfinds', 0)
                self.total_items_dumped = data.get('total_items_dumped', 0)
                self.total_items_dumpfinds = data.get('total_items_dumpfinds', 0)
                self.total_items_marketbought = data.get('total_items_marketbought', 0)
                self.total_items_sent = data.get('total_items_sent', 0)
                self.total_jail_bailcosts = data.get('total_jail_bailcosts', 0)
                self.total_jail_bailed = data.get('total_jail_bailed', 0)
                self.total_jail_busted = data.get('total_jail_busted', 0)
                self.total_jail_busts = data.get('total_jail_busts', 0)
                self.total_jail_jailed = data.get('total_jail_jailed', 0)
                self.total_mails_sent = data.get('total_mails_sent', 0)
                self.total_mails_sent_company = data.get('total_mails_sent_company', 0)
                self.total_mails_sent_faction = data.get('total_mails_sent_faction', 0)
                self.total_mails_sent_friends = data.get('total_mails_sent_friends', 0)
                self.total_mails_sent_spouse = data.get('total_mails_sent_spouse', 0)
                self.total_merits_bought = data.get('total_merits_bought', 0)
                self.total_points_boughttotal = data.get('total_points_boughttotal', 0)
                self.total_refills_bought = data.get('total_refills_bought', 0)
                self.total_statenhancers_used = data.get('total_statenhancers_used', 0)
                self.total_trades = data.get('total_trades', 0)
                self.total_travel_all = data.get('total_travel_all', 0)
                self.total_travel_argentina = data.get('total_travel_argentina', 0)
                self.total_travel_canada = data.get('total_travel_canada', 0)
                self.total_travel_caymanislands = data.get('total_travel_caymanislands', 0)
                self.total_travel_china = data.get('total_travel_china', 0)
                self.total_travel_dubai = data.get('total_travel_dubai', 0)
                self.total_travel_hawaii = data.get('total_travel_hawaii', 0)
                self.total_travel_japan = data.get('total_travel_japan', 0)
                self.total_travel_mexico = data.get('total_travel_mexico', 0)
                self.total_travel_southafrica = data.get('total_travel_southafrica', 0)
                self.total_travel_switzerland = data.get('total_travel_switzerland', 0)
                self.total_travel_unitedkingdom = data.get('total_travel_unitedkingdom', 0)
                self.total_users_logins = data.get('total_users_logins', 0)
                self.total_users_playtime = data.get('total_users_playtime', 0)
                self.users_daily = data.get('users_daily', 0)
                self.users_enby = data.get('users_enby', 0)
                self.users_female = data.get('users_female', 0)
                self.users_male = data.get('users_male', 0)
                self.users_marriedcouples = data.get('users_marriedcouples', 0)
                self.users_total = data.get('users_total', 0)
                self.wars_raid = data.get('wars_raid', 0)
                self.wars_ranked = data.get('wars_ranked', 0)
                self.wars_territory = data.get('wars_territory', 0)
                logger.debug(f"Processed StatsData: {self}")

            def __repr__(self):
                return f"StatsData(timestamp={self.timestamp}, users_total={self.users_total})"
    
    class Stocks:
        def __init__(self, api: TornAPI, id: Optional[int] = None):
            self.api = api
            self.id = id
            self.data = None
            logger.info("Initialized Stocks for Torn section")

        def fetch_data(self):
            """
            Fetch data for the Stocks using TornAPI.

            Returns:
            - Dict[str, Stock]: A dictionary of Stock instances, keyed by stock ID.
            """
            logger.debug("Fetching stocks data")

            try:
                response = self.api.make_request('torn', self.id, 'stocks')
                logger.debug(f"API response for stocks: {response}")

                if not response or 'stocks' not in response:
                    logger.warning("Stocks data not found in the response")
                    return None

                self.data = {stock_id: self.Stock(stock_data) for stock_id, stock_data in response['stocks'].items()}
                logger.info("Fetched stocks data successfully")
                return self.data

            except Exception as e:
                logger.error(f"Error fetching stocks data: {e}")
                return None

        class Stock:
            def __init__(self, data: Dict[str, Any]):
                """
                Parse and store the stock data.

                Args:
                - data: A dictionary containing the fetched stock data.
                """
                self.acronym = data.get('acronym', '')
                self.all_time = self.Price(data.get('all_time', {}))
                self.benefit = self.Benefit(data.get('benefit', {}))
                self.current_price = data.get('current_price', 0.0)
                self.history = [self.History(history_data) for history_data in data.get('history', [])]
                self.investors = data.get('investors', 0)
                self.last_day = self.Price(data.get('last_day', {}))
                self.last_hour = self.Price(data.get('last_hour', {}))
                self.last_month = self.Price(data.get('last_month', {}))
                self.last_week = self.Price(data.get('last_week', {}))
                self.last_year = self.Price(data.get('last_year', {}))
                self.market_cap = data.get('market_cap', 0)
                self.name = data.get('name', '')
                self.stock_id = data.get('stock_id', 0)
                self.total_shares = data.get('total_shares', 0)
                logger.debug(f"Processed Stock: {self}")

            def __repr__(self):
                return f"Stock(name='{self.name}', acronym='{self.acronym}', current_price={self.current_price})"

            class Benefit:
                def __init__(self, data: Dict[str, Any]):
                    self.description = data.get('description', '')
                    self.frequency = data.get('frequency', 0)
                    self.requirement = data.get('requirement', 0)
                    self.type = data.get('type', '')
                    logger.debug(f"Processed Benefit: {self}")

                def __repr__(self):
                    return f"Benefit(type='{self.type}', description='{self.description}')"

            class History:
                def __init__(self, data: Dict[str, Any]):
                    self.change = data.get('change', 0.0)
                    self.price = data.get('price', 0.0)
                    self.timestamp = data.get('timestamp', 0)
                    logger.debug(f"Processed History: {self}")

                def __repr__(self):
                    return f"History(price={self.price}, change={self.change}, timestamp={self.timestamp})"

            class Price:
                def __init__(self, data: Dict[str, Any]):
                    self.change = data.get('change', 0.0)
                    self.change_percentage = data.get('change_percentage', 0.0)
                    self.end = data.get('end', 0.0)
                    self.high = data.get('high', 0.0)
                    self.low = data.get('low', 0.0)
                    self.start = data.get('start', 0.0)
                    logger.debug(f"Processed Price: {self}")

                def __repr__(self):
                    return f"Price(start={self.start}, end={self.end}, high={self.high}, low={self.low}, change={self.change}, change_percentage={self.change_percentage})"
    
    class Territory:
        def __init__(self, api: TornAPI):
            self.api = api
            self.data = None
            logger.info("Initialized Territory for Torn section")

        def fetch_data(self, territory_names: List[str]):
            """
            Fetch data for the specified territories using TornAPI.

            Args:
            - territory_names (List[str]): A list of territory names to fetch data for.

            Returns:
            - Dict[str, Any]: A dictionary containing the fetched territory data.
            """
            logger.debug("Fetching territory data")

            if len(territory_names) > 50:
                logger.error("Cannot fetch data for more than 50 territories at a time")
                return None

            try:
                territory_ids = ','.join(territory_names)
                response = self.api.make_request('torn', territory_ids, 'territory')
                logger.debug(f"API response for territory: {response}")

                if not response or 'territory' not in response:
                    logger.warning("Territory data not found in the response")
                    return None

                self.data = response['territory']
                logger.info("Fetched territory data successfully")
                return self.data

            except Exception as e:
                logger.error(f"Error fetching territory data: {e}")
                return None

        class Racket:
            def __init__(self, data: Dict[str, Any]):
                self.changed = data.get('changed', 0)
                self.created = data.get('created', 0)
                self.level = data.get('level', 0)
                self.name = data.get('name', '')
                self.reward = data.get('reward', '')
                logger.debug(f"Processed Racket: {self}")

            def __repr__(self):
                return f"Racket(name='{self.name}', level={self.level}, reward='{self.reward}')"

        class TerritoryWar:
            def __init__(self, data: Dict[str, Any]):
                self.assaulting_faction = data.get('assaulting_faction', 0)
                self.defending_faction = data.get('defending_faction', 0)
                self.ends = data.get('ends', 0)
                self.required_score = data.get('required_score', 0)
                self.score = data.get('score', 0)
                self.started = data.get('started', 0)
                self.territory_war_id = data.get('territory_war_id', 0)
                logger.debug(f"Processed TerritoryWar: {self}")

            def __repr__(self):
                return f"TerritoryWar(assaulting_faction={self.assaulting_faction}, defending_faction={self.defending_faction}, ends={self.ends}, required_score={self.required_score}, score={self.score}, started={self.started}, territory_war_id={self.territory_war_id})"
    
    class TerritoryNames:
        def __init__(self, api: TornAPI):
            self.api = api
            self.data = None
            logger.info("Initialized TerritoryNames for Torn section")

        def fetch_data(self):
            """
            Fetch data for the TerritoryNames using TornAPI.

            Returns:
            - List[str]: A list of territory names.
            """
            logger.debug("Fetching territory names data")

            try:
                response = self.api.make_request('torn', '', 'territorynames')
                logger.debug(f"API response for territory names: {response}")

                if not response or 'territoryNames' not in response:
                    logger.warning("Territory names data not found in the response")
                    return None

                self.data = response['territoryNames']
                logger.info("Fetched territory names data successfully")
                return self.data

            except Exception as e:
                logger.error(f"Error fetching territory names data: {e}")
                return None

        def __repr__(self):
            return f"TerritoryNames(data={self.data})"

    class TerritoryWarReport:
        def __init__(self, api: TornAPI, id: int):
            self.api = api
            self.id = id
            self.data = None
            logger.info(f"Initialized TerritoryWarReport for Torn section with ID: {self.id}")

        def fetch_data(self):
            """
            Fetch data for the Territory War Report using TornAPI.

            Returns:
            - TerritoryWarReportData: An instance of TerritoryWarReportData containing the fetched data.
            """
            if self.id is None:
                logger.error("Territory war report ID is required but not provided")
                return None

            logger.debug(f"Fetching territory war report data for ID: {self.id}")

            try:
                response = self.api.make_request('torn', self.id, 'territorywarreport')
                logger.debug(f"API response for territory war report: {response}")

                if not response or 'territorywarreport' not in response:
                    logger.warning("Territory war report data not found in the response")
                    return None

                self.data = self.TerritoryWarReportData(response['territorywarreport'])
                logger.info(f"Fetched territory war report data successfully for ID: {self.id}")
                return self.data

            except Exception as e:
                logger.error(f"Error fetching territory war report data: {e}")
                return None

        class TerritoryWarReportData:
            def __init__(self, data: Dict[str, Any]):
                """
                Parse and store the territory war report data.

                Args:
                - data: A dictionary containing the fetched territory war report data.
                """
                self.factions = {faction_id: self.Faction(faction_data) for faction_id, faction_data in data.get('factions', {}).items()}
                self.territory = self.Territory(data.get('territory', {}))
                self.war = self.War(data.get('war', {}))
                logger.debug(f"Processed TerritoryWarReportData: {self}")

            def __repr__(self):
                return f"TerritoryWarReportData(factions={self.factions}, territory={self.territory}, war={self.war})"

            class Faction:
                def __init__(self, data: Dict[str, Any]):
                    self.clears = data.get('clears', 0)
                    self.joins = data.get('joins', 0)
                    self.members = {user_id: self.User(user_data) for user_id, user_data in data.get('members', {}).items()}
                    self.name = data.get('name', '')
                    self.score = data.get('score', 0)
                    self.type = data.get('type', '')
                    logger.debug(f"Processed Faction: {self}")

                def __repr__(self):
                    return f"Faction(name='{self.name}', score={self.score}, type='{self.type}')"

                class User:
                    def __init__(self, data: Dict[str, Any]):
                        self.clears = data.get('clears', 0.0)
                        self.faction_id = data.get('faction_id', 0)
                        self.joins = data.get('joins', 0.0)
                        self.level = data.get('level', 0)
                        self.name = data.get('name', '')
                        self.points = data.get('points', 0)
                        logger.debug(f"Processed User: {self}")

                    def __repr__(self):
                        return f"User(name='{self.name}', points={self.points})"

            class Territory:
                def __init__(self, data: Dict[str, Any]):
                    self.name = data.get('name', '')
                    logger.debug(f"Processed Territory: {self}")

                def __repr__(self):
                    return f"Territory(name='{self.name}')"

            class War:
                def __init__(self, data: Dict[str, Any]):
                    self.end = data.get('end', 0)
                    self.result = data.get('result', '')
                    self.start = data.get('start', 0)
                    self.winner = data.get('winner', 0)
                    logger.debug(f"Processed War: {self}")

                def __repr__(self):
                    return f"War(start={self.start}, end={self.end}, result='{self.result}', winner={self.winner})"

                    def __init__(self, data: Dict[str, Any]):
                        self.assaulting_faction = data.get('assaulting_faction', 0)
                        self.defending_faction = data.get('defending_faction', 0)
                        self.ends = data.get('ends', 0)
                        self.required_score = data.get('required_score', 0)
                        self.score = data.get('score', 0)
                        self.started = data.get('started', 0)
                        self.territory_war_id = data.get('territory_war_id', 0)
                        logger.debug(f"Processed TerritoryWar: {self}")

                    def __repr__(self):
                        return (f"TerritoryWar(assaulting_faction={self.assaulting_faction}, "
                                f"defending_faction={self.defending_faction}, ends={self.ends}, "
                                f"required_score={self.required_score}, score={self.score}, "
                                f"started={self.started}, territory_war_id={self.territory_war_id})")
        
    class TerritoryWars:
        def __init__(self, api: TornAPI):
            self.api = api
            self.data = None
            logger.info("Initialized TerritoryWars for Torn section")

        def fetch_data(self):
            """
            Fetch data for the TerritoryWars using TornAPI.

            Returns:
            - Dict[str, TerritoryWar]: A dictionary of TerritoryWar instances, keyed by territory.
            """
            logger.debug("Fetching territory wars data")

            try:
                response = self.api.make_request('torn', '', 'territorywars')
                logger.debug(f"API response for territory wars: {response}")

                if not response or 'territorywars' not in response:
                    logger.warning("Territory wars data not found in the response")
                    return None

                self.data = {territory: self.TerritoryWar(war_data) for territory, war_data in response['territorywars'].items()}
                logger.info("Fetched territory wars data successfully")
                return self.data

            except Exception as e:
                logger.error(f"Error fetching territory wars data: {e}")
                return None

        class TerritoryWar:
            def __init__(self, data: Dict[str, Any]):
                self.assaulting_faction = data.get('assaulting_faction', 0)
                self.defending_faction = data.get('defending_faction', 0)
                self.ends = data.get('ends', 0)
                self.required_score = data.get('required_score', 0)
                self.score = data.get('score', 0)
                self.started = data.get('started', 0)
                self.territory_war_id = data.get('territory_war_id', 0)
                logger.debug(f"Processed TerritoryWar: {self}")

            def __repr__(self):
                return (f"TerritoryWar(assaulting_faction={self.assaulting_faction}, "
                        f"defending_faction={self.defending_faction}, ends={self.ends}, "
                        f"required_score={self.required_score}, score={self.score}, "
                        f"started={self.started}, territory_war_id={self.territory_war_id})")

    class Timestamp:
        def __init__(self):
            self.timestamp = int(datetime.now().timestamp())
            logger.info(f"Initialized Timestamp with value: {self.timestamp}")

        def fetch_data(self):
            """
            Get the current time as an epoch timestamp in seconds.

            Returns:
            - int: The current epoch timestamp in seconds.
            """
            self.timestamp = int(datetime.now().timestamp())
            logger.debug(f"Updated Timestamp to current value: {self.timestamp}")
            return self.timestamp

        def __repr__(self):
            return f"Timestamp(timestamp={self.timestamp})"
                
                
            
if __name__ == "__main__":
     api = TornAPI()
