import functools
import time
from requests.exceptions import RequestException

class AIAgentError(Exception):
    """Base exception class for AI Agent errors."""
    pass

class CryptoAPIError(AIAgentError):
    """Exception raised for errors in the Crypto API."""
    pass

class LLMError(AIAgentError):
    """Exception raised for errors in the Language Model."""
    pass

class RateLimitError(AIAgentError):
    """Exception raised when rate limits are exceeded."""
    pass

def retry_with_exponential_backoff(max_retries=3, base_delay=1):
    """
    Decorator for retrying a function with exponential backoff.
    
    Args:
    max_retries (int): Maximum number of retries
    base_delay (int): Base delay in seconds
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(max_retries + 1):
                try:
                    return func(*args, **kwargs)
                except (RequestException, CryptoAPIError, LLMError, RateLimitError) as e:
                    if attempt == max_retries:
                        raise AIAgentError(f"Max retries reached. Last error: {str(e)}")
                    delay = base_delay * (2 ** attempt)
                    print(f"Attempt {attempt + 1} failed. Retrying in {delay} seconds...")
                    time.sleep(delay)
            return func(*args, **kwargs)
        return wrapper
    return decorator

def handle_api_errors(func):
    """Decorator to handle API-related errors."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except RequestException as e:
            raise CryptoAPIError(f"Error in Crypto API request: {str(e)}")
        except Exception as e:
            if "together" in str(e).lower():
                raise LLMError(f"Error in LLM API request: {str(e)}")
            raise AIAgentError(f"Unexpected error: {str(e)}")
    return wrapper

def rate_limiter(max_calls, time_frame):
    """
    Decorator to implement basic rate limiting.
    
    Args:
    max_calls (int): Maximum number of calls allowed in the time frame
    time_frame (int): Time frame in seconds
    """
    calls = []
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            now = time.time()
            calls[:] = [c for c in calls if c > now - time_frame]
            if len(calls) >= max_calls:
                raise RateLimitError(f"Rate limit exceeded. Max {max_calls} calls per {time_frame} seconds.")
            calls.append(now)
            return func(*args, **kwargs)
        return wrapper
    return decorator

# Example usage
if __name__ == "__main__":
    @retry_with_exponential_backoff()
    @handle_api_errors
    #@rate_limiter(max_calls=5, time_frame=60)
    def example_function():
        # Simulating an API call that might fail
        import random
        if random.random() < 0.5:
            raise RequestException("Random API error")
        return "Success"

    try:
        result = example_function()
        print(result)
    except AIAgentError as e:
        print(f"Caught AIAgentError: {str(e)}")