# sections.py

import logging
from typing import Dict, Any
from main_api import TornAPI
from logger import setup_logger, close_logger

# Set up the logger for the sections module
logger, file_handler = setup_logger(name='sections', level=logging.CRITICAL)

class User:
    def __init__(self, api: TornAPI, user_id: int):
        self.api = api
        self.user_id = user_id
        self.ammo = self.Ammo(self.api, self.user_id)
        self.basic = self.Basic(self.api, self.user_id)
        logger.info(f"Initialized User with ID: {self.user_id}")

    class Ammo:
        def __init__(self, api: TornAPI, user_id: int):
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
        def __init__(self, api: TornAPI, user_id: int):
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

class Sections:
    def __init__(self, api: TornAPI):
        self.api = api
        logger.info("Initialized Sections")

    def user(self, user_id: int) -> User:
        """Return a User object initialized with the provided user_id."""
        logger.info(f"Creating User object for User ID: {user_id}")
        return User(self.api, user_id)

# Example usage
if __name__ == "__main__":
    api = TornAPI()
    sections = Sections(api)

    # Fetch user's basic info using user_id
    user = sections.user("")  # Replace with the actual user ID
    basic_info = user.basic.basic_data
    print(basic_info)

    # Close the logger
    close_logger(logger, file_handler)

    api.close()
