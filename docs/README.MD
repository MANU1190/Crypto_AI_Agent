# Crypto AI Assistant

## Overview
The **Crypto AI Assistant** is an intelligent conversational agent designed to provide real-time cryptocurrency price information and handle general queries. Powered by the **LLaMA 3.1 8B model** from Together AI and integrated with the CoinGecko API, it offers a seamless user experience through a Streamlit-based chat interface. The assistant combines API integration, prompt engineering, and a Reasoning + Acting (ReAct) approach to deliver accurate and context-aware responses.

---

## Features

### Core Features
- **Cryptocurrency Price Fetching**  
  - Fetches real-time prices for cryptocurrencies (e.g., Bitcoin, Ethereum) using the CoinGecko API.  
  - Gracefully handles invalid cryptocurrency names with clear error messages.  

- **Conversational Context Maintenance**  
  - Retains conversation history across multiple queries for natural, context-aware interactions.  

- **General Query Handling**  
  - Answers non-cryptocurrency-related questions using the LLaMA 3.1 8B model.  
  - Delivers concise and intelligent responses based on a predefined system prompt.  

- **ReAct Agent Integration**  
  - Implements Reasoning + Acting (ReAct) to determine whether to fetch prices or provide general knowledge.  
  - Displays reasoning steps in the terminal for debugging.  
---
### Explanation of Components
- **Streamlit UI**: A simple chat interface for user interaction.  
- **AI Agent**: The core logic that maintains conversation history and decides whether to fetch prices or use the LLM.  
- **Together AI (LLaMA 3.1 8B)**: Processes non-price-related queries and generates intelligent responses.  
- **Crypto API (CoinGecko)**: Provides real-time cryptocurrency price data.  

---

## Setup Instructions

### Prerequisites
- Python 3.9 or above  
- A Together AI account with an API key  
- Access to the CoinGecko API (publicly available)  

### Installation
1. **Clone the Repository**  
   ```bash
   git clone https://github.com/skpthe1/Crypto_AI_Agent.git
   cd crypto-ai-assistant
   ```

2. **Create a Virtual Environment**  
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. **Install Dependencies**  
   ```bash
   pip install -r requirements.txt
   ```

4. **Set Up Environment Variables**  
   ```bash
   # Create a .env file in the root directory with the following:
   TOGETHER_API_KEY=your_together_ai_api_key
   ```

5. **Run the Application**  
   ```bash
   streamlit run app.py
   ```

### Assumptions and Limitations

**Assumptions**  
- User queries are in English.  
- Cryptocurrency names generally match those recognized by CoinGecko (e.g., "bitcoin", "ethereum").  

**Limitations**  
- No real-time language translation for non-English inputs.  
- The ReAct agent may misinterpret ambiguous queries due to reliance on prompt engineering.  
- Dependent on public APIs (Together AI and CoinGecko), which may have rate limits or downtime.  

