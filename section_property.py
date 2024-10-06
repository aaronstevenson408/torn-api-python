from typing import Dict, Any, Optional
from tornApi import TornAPI
from env_loader import load_environment_variables
from logger import setup_logger, close_logger

env = load_environment_variables()
if env is None:
    raise ValueError("Failed to load environment variables.")
logger, file_handler = setup_logger('Sections', env['DEBUG_LEVEL'])

class Property:
    def __init__(self, api: TornAPI, property_id: Optional[int]):
        """
        Initialize the Property class with the TornAPI and property_id.

        Args:
        - api: An instance of the TornAPI class.
        - property_id: The ID of the property to fetch data for.
        """
        self.api = api
        self.property_id = property_id

        # Initialize the inner Property class for fetching property details
        self.property = self.Property(self.api, self.property_id)
        self.lookup = self.Lookup(self.api, self.property_id)   
        self.timestamp = self.Timestamp(self.api, self.property_id)

        logger.info(f"Initialized Property for Property ID: {self.property_id}")

    class Property:
        def __init__(self, api: TornAPI, property_id: Optional[int]):
            self.api = api
            self.property_id = property_id
            self.data = None
            logger.info(f"Initialized Property for Property ID: {self.property_id}")

        def fetch_data(self):
            """
            Fetch data for the Property using TornAPI.

            Returns:
            - PropertyData: An instance of PropertyData containing the fetched data.
            """
            logger.debug(f"Fetching property data for Property ID: {self.property_id}")

            try:
                # Make API request for the property selection
                response = self.api.make_request('property', self.property_id)
                logger.debug(f"API response for property selection: {response}")

                # Check if response contains valid data
                if not response:
                    logger.warning(f"Property data not found for Property ID: {self.property_id}")
                    return None

                # Parse and store data in the data holding class
                self.data = self.PropertyData(response)
                logger.info(f"Fetched property data for Property ID: {self.property_id}")
                return self.data

            except Exception as e:
                logger.error(f"Error fetching property data for Property ID: {self.property_id}: {e}")
                return None

        class PropertyData:
            def __init__(self, data: Dict[str, Any]):
                """
                Parse and store the property selection data.

                Args:
                - data: A dictionary containing the fetched property data.
                """
                # Parse fields from the response
                self.happy = data.get('happy', 0)
                self.owner_id = data.get('owner_id', 0)
                self.property_type = data.get('property_type', 0)
                self.rented = self.Rented(data.get('rented', {}))
                self.staff = data.get('staff', [])
                self.upgrades = data.get('upgrades', [])
                self.upkeep = data.get('upkeep', 0)
                self.users_living = data.get('users_living', 0)

                logger.debug(f"Processed PropertyData: {self}")

            class Rented:
                def __init__(self, data: Dict[str, Any]):
                    """
                    Parse and store the rented object data.

                    Args:
                    - data: A dictionary containing the rented data.
                    """
                    self.cost_per_day = data.get('cost_per_day', 0)
                    self.days_left = data.get('days_left', 0)
                    self.total_cost = data.get('total_cost', 0)
                    self.user_id = data.get('user_id', 0)

                    logger.debug(f"Processed Rented: {self}")

            def __repr__(self):
                return (f"PropertyData(happy={self.happy}, owner_id={self.owner_id}, "
                        f"property_type={self.property_type}, rented={self.rented}, "
                        f"staff={self.staff}, upgrades={self.upgrades}, "
                        f"upkeep={self.upkeep}, users_living={self.users_living})")


    class Lookup:
        def __init__(self, api: TornAPI, property_id: Optional[int]):
            """
            Initialize the Lookup class.

            Args:
            - api: An instance of the TornAPI class.
            - property_id: The ID of the property (not used for lookup, but kept for consistency).
            """
            self.api = api
            self.property_id = property_id
            self.data = None

            logger.info(f"Initialized Lookup for Property section")

        def fetch_data(self):
            """
            Fetch the available selections for the Property section.

            Returns:
            - LookupData: An instance of LookupData containing the fetched selections.
            """
            logger.debug("Fetching selections for Property section")

            try:
                # Make API request for the property lookup
                response = self.api.make_request('property', '', 'lookup')
                logger.debug(f"API response for property lookup: {response}")

                # Check if response contains valid data
                if not response or 'selections' not in response:
                    logger.warning("Selections data not found for Property section")
                    return None

                # Parse and store data in the data holding class
                self.data = self.LookupData(response)
                logger.info("Fetched selections for Property section")
                return self.data

            except Exception as e:
                logger.error(f"Error fetching selections for Property section: {e}")
                return None

        class LookupData:
            def __init__(self, data: Dict[str, Any]):
                """
                Parse and store the lookup data.

                Args:
                - data: A dictionary containing the fetched lookup data.
                """
                self.selections = data.get('selections', [])

                logger.debug(f"Processed LookupData: {self}")

            def __repr__(self):
                return f"LookupData(selections={self.selections})"
    class Timestamp:
        def __init__(self, api: TornAPI, property_id: Optional[int]):
            self.api = api
            self.property_id = property_id
            logger.info(f"Initialized Timestamp for Property ID: {self.property_id}")

        def fetch_data(self):  
            """
            Fetch the current timestamp for the property.

            Returns:
            - int: The current timestamp.
            """
            logger.debug(f"Fetching current timestamp for Property ID: {self.property_id}")

            try:
                # Make API request for the property timestamp
                response = self.api.make_request('property', self.property_id, 'timestamp')
                logger.debug(f"API response for property timestamp: {response}")

                # Check if response contains valid data
                if not response or 'timestamp' not in response:
                    logger.warning("Timestamp data not found for Property ID: {self.property_id}")
                    return None # TODO: Check if this is correct

                # Parse and store data in the data holding class
                self.data = self.TimestampData(response)
                logger.info("Fetched current timestamp for Property ID: {self.property_id}")
                return self.data

            except Exception as e:
                logger.error(f"Error fetching current timestamp for Property ID: {self.property_id}: {e}")
                return None # TODO: Check if this is correct

        class TimestampData:
            def __init__(self, data: Dict[str, Any]):
                """
                Parse and store the timestamp data.

                Args:
                - data: A dictionary containing the fetched timestamp data.
                """ 
                self.timestamp = data.get('timestamp', 0)

                logger.debug(f"Processed TimestampData: {self}")

            def __repr__(self):
                return f"TimestampData(timestamp={self.timestamp})" # TODO: Check if this is correct      
