# sections.py
# TODO: Format each selection to use a fecth class and a sub class of attributes
from typing import Dict, Any, Optional
from tornApi import TornAPI
from env_loader import load_environment_variables
from logger import setup_logger, close_logger

env = load_environment_variables()
if env is None:
    raise ValueError("Failed to load environment variables.")
logger, file_handler = setup_logger('Sections', env['DEBUG_LEVEL'])

from section_user import User
from section_property import Property
from section_market import Market
from section_torn import Torn

class Sections:
    def __init__(self, api: TornAPI):
        self.api = api
        logger.info("Initialized Sections")

    def user(self, user_id: Optional[int] = None) -> User:
        """Return a User object initialized with the provided user_id."""
        logger.info(f"Creating User object for User ID: {user_id}")
        return User(self.api, user_id)

    def property(self, property_id: Optional[int] = None) -> Property:
        """Return a Property object initialized with the provided property_id."""
        logger.info(f"Creating Property object for Property ID: {property_id}")
        return Property(self.api, property_id)

    def market(self, item_id: Optional[int] = None) -> Market:
        """Return a Market object initialized with the provided item_id."""
        logger.info(f"Creating Market object for Item ID: {item_id}")
        return Market(self.api, item_id)
    
    
    def torn(self, id: Optional[int] = None) -> Torn:
        """Return a Torn object initialized with the provided selection and id."""
        logger.info(f"Creating Torn object for ID: {id}")
        return Torn(self.api,id)
    
    