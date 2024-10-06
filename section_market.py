from typing import Dict, Any, Optional
from tornApi import TornAPI
from env_loader import load_environment_variables
from logger import setup_logger, close_logger

env = load_environment_variables()
if env is None:
    raise ValueError("Failed to load environment variables.")
logger, file_handler = setup_logger('Sections', env['DEBUG_LEVEL'])


class Market:
    def __init__(self, api: TornAPI, item_id: Optional[int]):
        self.api = api
        self.item_id = item_id
        logger.info(f"Initialized Market for Item ID: {self.item_id}")

        # Initialize the inner classes for each selection
        self.bazaar = self.Bazaar(self.api, self.item_id)
        self.itemmarket = self.ItemMarket(self.api, self.item_id)
        self.lookup = self.Lookup(self.api)
        self.pointsmarket = self.PointsMarket(self.api)
        self.timestamp = self.Timestamp(self.api)

    class Bazaar:
        def __init__(self, api: TornAPI, item_id: Optional[int]):
            self.api = api
            self.item_id = item_id
            self.data = None
            logger.info(f"Initialized Bazaar for Item ID: {self.item_id}")

        def fetch_data(self):
            """Fetch bazaar data for the specified item."""
            logger.debug(f"Fetching bazaar data for Item ID: {self.item_id}")
            try:
                response = self.api.make_request('market', self.item_id, 'bazaar')
                if response and 'bazaar' in response:
                    self.data = self.BazaarData(response)
                    logger.info(f"Fetched bazaar data for Item ID: {self.item_id}")
                    return self.data
                else:
                    logger.warning(f"No bazaar data found for Item ID: {self.item_id}")
                    return None
            except Exception as e:
                logger.error(f"Error fetching bazaar data for Item ID: {self.item_id}: {e}")
                return None

        class BazaarData:
            def __init__(self, data: Dict[str, Any]):
                self.bazaar = [self.BazaarItem(item) for item in data.get('bazaar', [])]
                logger.debug(f"Processed BazaarData: {self}")

            class BazaarItem:
                def __init__(self, item: Dict[str, Any]):
                    self.cost = item.get('cost', 0)
                    self.quantity = item.get('quantity', 0)

            def __repr__(self):
                return f"BazaarData(bazaar_items={len(self.bazaar)})"

            def __str__(self):
                return f"Bazaar offers: {[{'cost': item.cost, 'quantity': item.quantity} for item in self.bazaar]}"

    class ItemMarket:
        def __init__(self, api: TornAPI, item_id: Optional[int]):
            self.api = api
            self.item_id = item_id
            self.data = None
            logger.info(f"Initialized ItemMarket for Item ID: {self.item_id}")

        def fetch_data(self):
            """Fetch item market data for the specified item."""
            logger.debug(f"Fetching item market data for Item ID: {self.item_id}")
            try:
                response = self.api.make_request('market', self.item_id, 'itemmarket')
                if response and 'itemmarket' in response:
                    self.data = self.ItemMarketData(response)
                    logger.info(f"Fetched item market data for Item ID: {self.item_id}")
                    return self.data
                else:
                    logger.warning(f"No item market data found for Item ID: {self.item_id}")
                    return None
            except Exception as e:
                logger.error(f"Error fetching item market data for Item ID: {self.item_id}: {e}")
                return None

        class ItemMarketData:
            def __init__(self, data: Dict[str, Any]):
                self.itemmarket = [self.MarketItem(item) for item in data.get('itemmarket', [])]
                logger.debug(f"Processed ItemMarketData: {self}")

            class MarketItem:
                def __init__(self, item: Dict[str, Any]):
                    self.cost = item.get('cost', 0)
                    self.quantity = item.get('quantity', 0)

            def __repr__(self):
                return f"ItemMarketData(market_items={len(self.itemmarket)})"

            def __str__(self):
                return f"Item market offers: {[{'cost': item.cost, 'quantity': item.quantity} for item in self.itemmarket]}"

    class Lookup:
        def __init__(self, api: TornAPI):
            self.api = api
            self.data = None
            logger.info("Initialized Market Lookup")

        def fetch_data(self):
            """Fetch market lookup data."""
            logger.debug("Fetching market lookup data")
            try:
                response = self.api.make_request('market', '', 'lookup')
                if response and 'selections' in response:
                    self.data = self.LookupData(response)
                    logger.info("Fetched market lookup data")
                    return self.data
                else:
                    logger.warning("No market lookup data found")
                    return None
            except Exception as e:
                logger.error(f"Error fetching market lookup data: {e}")
                return None

        class LookupData:
            def __init__(self, data: Dict[str, Any]):
                self.selections = data.get('selections', [])
                logger.debug(f"Processed LookupData: {self}")

            def __repr__(self):
                return f"LookupData(selections_count={len(self.selections)})"

            def __str__(self):
                return f"Market selections: {self.selections}"

    class PointsMarket:
        def __init__(self, api: TornAPI):
            self.api = api
            self.data = None
            logger.info("Initialized PointsMarket")

        def fetch_data(self):
            """Fetch points market data."""
            logger.debug("Fetching points market data")
            try:
                response = self.api.make_request('market', '', 'pointsmarket')
                if response and 'pointsmarket' in response:
                    self.data = self.PointsMarketData(response['pointsmarket'])
                    logger.info("Fetched points market data")
                    return self.data
                else:
                    logger.warning("No points market data found")
                    return None
            except Exception as e:
                logger.error(f"Error fetching points market data: {e}")
                return None

        class PointsMarketData:
            def __init__(self, data: Dict[str, Any]):
                self.points = {id: self.Point(point_data) for id, point_data in data.items()}
                logger.debug(f"Processed PointsMarketData: {self}")

            class Point:
                def __init__(self, point: Dict[str, Any]):
                    self.cost = point.get('cost', 0)
                    self.quantity = point.get('quantity', 0)
                    self.total_cost = point.get('total_cost', 0)

            def __repr__(self):
                return f"PointsMarketData(points_items={len(self.points)})"

            def __str__(self):
                return f"Points market offers: {[{'id': id, 'cost': point.cost, 'quantity': point.quantity, 'total_cost': point.total_cost} for id, point in self.points.items()]}"
    
    class Timestamp:
        def __init__(self, api: TornAPI):
            self.api = api
            self.data = None
            logger.info("Initialized Market Timestamp")

        def fetch_data(self):
            """Fetch market timestamp."""
            logger.debug("Fetching market timestamp")
            try:
                response = self.api.make_request('market', '', 'timestamp')
                if response and 'timestamp' in response:
                    self.data = response['timestamp']
                    logger.info("Fetched market timestamp")
                    return self.data
                else:
                    logger.warning("No market timestamp found")
                    return None
            except Exception as e:
                logger.error(f"Error fetching market timestamp: {e}")
                return None

        def __repr__(self):
            return f"Timestamp(timestamp={self.data})"



