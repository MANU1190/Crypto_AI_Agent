import streamlit as st
import os
import sys

# Add project root to Python path
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, PROJECT_ROOT)

from dotenv import load_dotenv
from services.ai_handler import AIAgent
from utils.session_manager import SessionManager

load_dotenv()

def main():
    st.title("Crypto AI Assistant")
    session_manager = SessionManager()

    ai_agent = AIAgent()

    if prompt := st.chat_input("Ask me anything"):
        session_manager.add_message("user", prompt)

        response = ai_agent.process_query(prompt)
        session_manager.add_message("assistant", response)
        
        session_manager.display_messages()

if __name__ == "__main__":
    main()