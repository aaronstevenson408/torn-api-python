# env_loader.py

import os
from dotenv import load_dotenv
import logging

def load_environment_variables(env_file='.env'):
    """
    Load environment variables from a .env file.
    
    Args:
        env_file (str): The path to the .env file. Defaults to '.env'.
    
    Returns:
        dict: A dictionary containing the debug level and API keys.
    """
    try:
        load_dotenv(env_file)
        logging.info(f"Environment variables loaded from {env_file}")
        
        # Retrieve the debug level
        debug_level = os.getenv('DEBUG_LEVEL', 'WARNING').upper()

        # Retrieve API keys for different access levels
        api_keys = {
            'full': os.getenv('Full'),
            'limited': os.getenv('Limited'),
            'min': os.getenv('Min'),
            'public': os.getenv('Public')
        }
        
        return {
            'DEBUG_LEVEL': debug_level,
            'API_KEYS': api_keys
        }
    except Exception as e:
        logging.error(f"Error loading environment variables: {e}")
        return None
