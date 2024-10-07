import time
from env_loader import load_environment_variables
from logger import setup_logger
# TODO: Implement wait time if limit is exceeded or fix the rate limiter
class RateLimiter:
    def __init__(self, limit=100, timeframe=60):
        """
        Initializes the rate limiter.
        
        :param limit: Maximum number of requests allowed in the specified timeframe.
        :param timeframe: Timeframe in seconds for the limit.
        """
        self.limit = limit  # Maximum requests allowed
        self.timeframe = timeframe  # Timeframe in seconds
        self.requests = []  # List to track timestamps of requests
        env = load_environment_variables()
        if env is None:
            raise ValueError("Failed to load environment variables.")

        self.logger, self.file_handler = setup_logger('RateLimiter', env['DEBUG_LEVEL'])

    def _clean_up(self):
        """Remove timestamps older than the timeframe."""
        current_time = time.time()
        # This keeps only the requests that are within the timeframe
        self.requests = [req for req in self.requests if current_time - req < self.timeframe]

    def request_allowed(self):
        """Check if a new request can be made."""
        self._clean_up()  # Clean up old requests
        # Check if the limit has been exceeded
        return len(self.requests) < self.limit

    def log_request(self):
        """Log the current request timestamp."""
        if self.request_allowed():
            self.requests.append(time.time())  # Record the time of the request
        else:
            self.logger.debug("Request limit exceeded")
            raise Exception("Request limit exceeded")  # Raise an error if the limit is exceeded


# # Usage
# rate_limiter = RateLimiter()

# try:
#     if rate_limiter.request_allowed():
#         # Make your API call here
#         logger.info("Request is allowed.")
#         rate_limiter.log_request()  # Log the request if it's allowed
#     else:
#         print("Request limit exceeded")
# except Exception as e:
#     print(e)
