import requests
import json
from datetime import datetime, timedelta

class CryptoAPI:
    def __init__(self, api_url="https://api.coingecko.com/api/v3", cache_expiry=60):
        self.api_url = api_url
        self.cache = {}
        self.cache_expiry = cache_expiry

    def get_price(self, coin_id: str, currency: str = "usd") -> float:
        """
        Fetches the current price of a cryptocurrency.

        Args:
            coin_id: The ID of the cryptocurrency (e.g., 'bitcoin', 'ethereum').
            currency: The currency to fetch the price in (default: 'usd').

        Returns:
            The price of the cryptocurrency in the specified currency as a float.

        Raises:
            ValueError: If the cryptocurrency is not found or an error occurs.
        """
        if coin_id in self.cache:
            data = self.cache[coin_id]
            if datetime.now() - data['timestamp'] < timedelta(seconds=self.cache_expiry):
                return data['price']

        url = f"{self.api_url}/simple/price"
        params = {"ids": coin_id, "vs_currencies": currency}
        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            if coin_id in data and currency in data[coin_id]:
                price = data[coin_id][currency]
                self.cache[coin_id] = {'price': price, 'timestamp': datetime.now()}
                return float(price)
            else:
                raise ValueError(f"Cryptocurrency '{coin_id}' not found.")
        except Exception as e:
            raise ValueError(f"Failed to fetch price for '{coin_id}': {str(e)}")

if __name__ == '__main__':
    crypto_api = CryptoAPI()
    try:
        bitcoin_price = crypto_api.get_price("bitcoin")
        print(f"The current price of Bitcoin is: ${bitcoin_price:.2f}")

        ethereum_price = crypto_api.get_price("ethereum")
        print(f"The current price of Ethereum is: ${ethereum_price:.2f}")

    except ValueError as e:
        print(f"Error: {e}")