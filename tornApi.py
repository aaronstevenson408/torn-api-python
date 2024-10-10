import requests
import time
from collections import deque
from threading import Lock
from urllib.parse import urlencode
from logger import setup_logger
from env_loader import load_environment_variables
# from rate_limiter import RateLimiter
from functools import lru_cache

class TornAPI:
    def __init__(self, access_level='full'):
        # Load environment variables
        env = load_environment_variables()
        if env is None:
            raise ValueError("Failed to load environment variables.")

        # Set up logger with the specified debug level
        self.logger, self.file_handler = setup_logger('TornAPI', env['DEBUG_LEVEL'])
        
        # Initialize the rate limiter
        self.rate_limiter = RateLimiter(limit=90, timeframe=60, backoff_factor=2)  # Adjusted limit for safety

        # Retrieve the API key based on the specified access level
        self.api_key = env['API_KEYS'].get(access_level)
        if not self.api_key:
            self.logger.error(f"API key for access level '{access_level}' not found.")
            raise ValueError("API key is required for the specified access level.")

        self.logger.info("TornAPI initialized with access level: %s", access_level)

    @lru_cache(maxsize=128)
    def _get_cache_key(self, section, id, selections, parameters):
        """Generate a unique cache key based on request parameters."""
        params = {'section': section, 'id': id, 'selections': selections}
        if parameters:
            params.update(parameters)
        return urlencode(sorted(params.items()))

    def make_request(self, section, id, selections=None, parameters=None):
        # Generate cache key
        cache_key = self._get_cache_key(section, id, selections, frozenset(parameters.items()) if parameters else None)
        
        # Check cache
        cached_response = self._get_from_cache(cache_key)
        if cached_response:
            self.logger.info(f"Using cached response for {cache_key}")
            return cached_response

        while True:
            self.rate_limiter.wait_for_next_request()
            self.rate_limiter.log_request()
            
            # Base URL
            url = f"https://api.torn.com/{section}/{id}"

            # Query parameters dictionary
            query_params = {'key': self.api_key}

            # Add selections if available
            if selections:
                if isinstance(selections, (list, tuple)):
                    query_params['selections'] = ','.join(selections)
                elif isinstance(selections, str):
                    query_params['selections'] = selections
                else:
                    self.logger.warning(f"Invalid selections type: {type(selections)}. Expected list, tuple, or string.")

            # Add additional parameters if provided
            if parameters:
                query_params.update(parameters)

            # Construct the full URL with encoded query parameters
            url += f"?{urlencode(query_params)}"
            
            self.logger.info(f"Making request to {url}")

            try:
                # Make the GET request
                response = requests.get(url)
                response.raise_for_status()
                self.logger.info(f"Received response: {response.status_code}")

                json_response = response.json()
                self.logger.info(f"Response data: {json_response}")  # Log the full response

                # Handle error in the response
                if 'error' in json_response:
                    error_code = json_response['error']['code']
                    error_message = self.interpret_error(error_code)
                    self.logger.error(f"Error occurred: {error_message}")
                    
                    if error_code == 5:  # Too many requests (rate limit hit)
                        self.rate_limiter.increase_wait_time()
                        continue  # Retry the request
                    
                    return None

                # Cache the successful response
                self._add_to_cache(cache_key, json_response)

                return json_response
                
            except requests.exceptions.RequestException as e:
                self.logger.error(f"Request failed: {e}")
                return None

    def _get_from_cache(self, key):
        """Retrieve a response from the cache if available."""
        # Implement a simple time-based cache
        current_time = time.time()
        if hasattr(self, 'cache') and key in self.cache:
            cached_time, data = self.cache[key]
            if current_time - cached_time < 30:  # 30 seconds cache duration
                return data
            else:
                del self.cache[key]
        return None

    def _add_to_cache(self, key, data):
        """Add a response to the cache."""
        if not hasattr(self, 'cache'):
            self.cache = {}
        self.cache[key] = (time.time(), data)

    def close(self):
        """Close the logger handlers to free resources."""
        if self.file_handler:
            self.logger.removeHandler(self.file_handler)
            self.file_handler.close()

    def interpret_error(self, error_code):
        """Interprets the error code from the TornAPI response."""
        error_messages = {
            0: "Unknown error. An unhandled error has occurred.",
            1: "Key is empty. Please provide a valid API key.",
            2: "Incorrect key. The provided API key is invalid.",
            3: "Wrong type. The requested type is incorrect.",
            4: "Wrong fields. Invalid selection fields were requested.",
            5: "Too many requests. Requests are blocked due to exceeding the limit.",
            6: "Incorrect ID. The ID provided is invalid.",
            7: "Incorrect ID-entity relation. The requested selection is private.",
            8: "IP block. Your IP has been temporarily banned due to abuse.",
            9: "API disabled. The API system is currently disabled.",
            10: "Key owner is in federal jail. This key cannot be used.",
            11: "Key change error. You can only change your API key once every 60 seconds.",
            12: "Key read error. There was an error reading the key from the database.",
            13: "The key is temporarily disabled due to inactivity.",
            14: "Daily read limit reached. You have exceeded your daily quota.",
            15: "Temporary error. An error code for testing purposes.",
            16: "Access level of this key is not high enough. You do not have permission to access this data.",
            17: "Backend error occurred. Please try again.",
            18: "API key is paused. The API key is currently inactive."
        }
        
        return error_messages.get(error_code, "Unknown error code. Please check the API documentation.")

class RateLimiter:
    def __init__(self, limit=90, timeframe=60, backoff_factor=2):
        """
        Initializes the rate limiter.
        
        :param limit: Maximum number of requests allowed in the specified timeframe.
        :param timeframe: Timeframe in seconds for the limit.
        :param backoff_factor: Factor to multiply wait time when rate limited.
        """
        self.limit = limit
        self.timeframe = timeframe
        self.backoff_factor = backoff_factor
        self.requests = deque()
        self.current_wait_time = 0
        self.lock = Lock()
        env = load_environment_variables()
        if env is None:
            raise ValueError("Failed to load environment variables.")

        self.logger, self.file_handler = setup_logger('RateLimiter', env['DEBUG_LEVEL'])

    def _clean_up(self):
        """Remove requests older than the timeframe."""
        current_time = time.time()
        while self.requests and current_time - self.requests[0] > self.timeframe:
            self.requests.popleft()

    def log_request(self):
        """Log the current request timestamp."""
        with self.lock:
            self._clean_up()
            self.requests.append(time.time())
            self.logger.debug(f"Request logged. Current count: {len(self.requests)}")

    def wait_for_next_request(self):
        """Wait until the next request is allowed."""
        with self.lock:
            self._clean_up()
            if len(self.requests) >= self.limit:
                wait_time = self.timeframe - (time.time() - self.requests[0])
                wait_time = max(wait_time, self.current_wait_time)
                self.logger.warning(f"Rate limit reached. Waiting {wait_time:.2f} seconds before next request...")
                time.sleep(wait_time)
                self.current_wait_time = self.current_wait_time * self.backoff_factor
            else:
                self.current_wait_time = 0

    def increase_wait_time(self):
        """Increase the wait time when a rate limit is hit."""
        with self.lock:
            self.current_wait_time = max(self.timeframe, self.current_wait_time * self.backoff_factor)
            self.logger.warning(f"Rate limit hit. Increasing wait time to {self.current_wait_time:.2f} seconds.")

# Note: IP Limit of 1,000 calls per minute is not implemented here.
# This would require tracking requests across all instances of TornAPI.

# Example usage
if __name__ == "__main__":
    try:
        access_level = 'full'  # Change this as needed
        api = TornAPI(access_level=access_level)
        
        # Example call to make_request (adjust parameters as needed)
        response = api.make_request('user', '', 'basic,attacks',{'to':'1727407808','from':'1727407808'})
        response2 = api.make_request('user', '', 'basic,attacks')
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        api.close()  # Ensure to close the logger