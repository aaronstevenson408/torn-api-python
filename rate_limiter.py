import time

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
            raise Exception("Request limit exceeded")  # Raise an error if the limit is exceeded


# Usage
rate_limiter = RateLimiter()

try:
    if rate_limiter.request_allowed():
        # Make your API call here
        print("Request is allowed")
        rate_limiter.log_request()  # Log the request if it's allowed
    else:
        print("Request limit exceeded")
except Exception as e:
    print(e)
