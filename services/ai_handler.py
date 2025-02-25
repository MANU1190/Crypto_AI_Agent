import os
import sys
import re  # Import regular expression module

# Add project root to Python path
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, PROJECT_ROOT)

from dotenv import load_dotenv
from together import Together
from services.crypto_api import CryptoAPI  # Absolute import (after adding to sys.path)

load_dotenv()

class AIAgent:
    def __init__(self):
        """Initializes the AIAgent with API keys, LLM client, and crypto API."""
        self.api_key = os.getenv("TOGETHER_API_KEY")
        if not self.api_key:
            raise ValueError("TOGETHER_API_KEY not found in environment variables.")
        self.client = Together(api_key=self.api_key)
        self.crypto_api = CryptoAPI()
        self.system_prompt = self._load_system_prompt()  # Load from file
        self.conversation_history = []  # To maintain context across conversations

    def _load_system_prompt(self):
        """Load the system prompt from the system_prompt.txt file."""
        try:
            with open("assets/system_prompt.txt", "r") as f:
                return f.read().strip()
        except FileNotFoundError:
            return "You are a helpful cryptocurrency assistant."  # Default prompt

    def process_query(self, query: str) -> str:
        """Processes a user query using ReAct and returns a response."""
        try:
            # Add user query to conversation history
            self.conversation_history.append({"role": "user", "content": query})

            # Use regular expressions to extract cryptocurrency name
            match = re.search(r"(price of|what is the price of|give me the price of)\s*(\w+)", query.lower())
            if match:
                coin_id = match.group(2).lower()  # Extract cryptocurrency name

                try:
                    price = self.crypto_api.get_price(coin_id)
                    response = f"The current price of {coin_id} is ${price:.2f}"
                except ValueError as e:
                    response = str(e)  # Handle invalid cryptocurrencies gracefully
            else:
                # For non-price-related queries, use LLM
                messages = [{"role": "system", "content": self.system_prompt}] + self.conversation_history + [
                    {"role": "user", "content": query}
                ]
                response = self.client.chat.completions.create(
                    model="meta-llama/Llama-3-8b-chat-hf",
                    messages=messages
                ).choices[0].message.content

            # Add assistant's response to conversation history
            self.conversation_history.append({"role": "assistant", "content": response})

            return response

        except Exception as e:
            return f"An unexpected error occurred: {str(e)}"

if __name__ == '__main__':
    agent = AIAgent()
    print(agent.process_query("What is the price of Bitcoin?"))
    print(agent.process_query("And Ethereum?"))
    print(agent.process_query("Who am I?"))