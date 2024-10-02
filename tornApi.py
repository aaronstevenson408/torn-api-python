import requests
from urllib.parse import urlencode
from logger import setup_logger
from env_loader import load_environment_variables
from rate_limiter import RateLimiter

class TornAPI:
    def __init__(self, access_level='full'):
        # Load environment variables
        env = load_environment_variables()
        if env is None:
            raise ValueError("Failed to load environment variables.")

        # Set up logger with the specified debug level
        self.logger, self.file_handler = setup_logger('TornAPI', env['DEBUG_LEVEL'])
        
        # Initialize the rate limiter
        self.rate_limiter = RateLimiter(limit=100, timeframe=60)  # Adjust as necessary

        # Retrieve the API key based on the specified access level
        self.api_key = env['API_KEYS'].get(access_level)
        if not self.api_key:
            self.logger.error(f"API key for access level '{access_level}' not found.")
            raise ValueError("API key is required for the specified access level.")

        self.logger.info("TornAPI initialized with access level: %s", access_level)

    def make_request(self, section, id, selections=None, parameters=None):
        # Ensure the rate limiter allows the request
        if self.rate_limiter.request_allowed():
            self.logger.info("Request is allowed.")
            self.rate_limiter.log_request()

            # Base URL
            url = f"https://api.torn.com/{section}/{id}"

            # Query parameters dictionary
            query_params = {'key': self.api_key}

            # Add selections if available
            if selections:
                query_params['selections'] = selections

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
                    self.logger.error(f"Error occurred: {self.interpret_error(error_code)}")
                    return None

                return json_response
            
            except requests.exceptions.RequestException as e:
                self.logger.error(f"Request failed: {e}")
                return None
        else:
            self.logger.warning("Rate limit exceeded. Request not allowed.")
            return None

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
