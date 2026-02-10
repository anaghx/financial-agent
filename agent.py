import os
import requests
import yfinance as yf
from dotenv import load_dotenv
from langchain_groq import ChatGroq

# ----------------------------
# Load environment variables
# ----------------------------
load_dotenv()

# ----------------------------
# Initialize Groq LLM
# ----------------------------
llm = ChatGroq(
    groq_api_key=os.getenv("GROQ_API_KEY"),
    model_name="llama-3.1-8b-instant"
)

# ----------------------------
# Country → Currency Mapping
# ----------------------------
country_currency_map = {
    "japan": "JPY",
    "india": "INR",
    "us": "USD",
    "usa": "USD",
    "united states": "USD",
    "uk": "GBP",
    "united kingdom": "GBP",
    "china": "CNY",
    "south korea": "KRW"
}

# ----------------------------
# Country → Index Mapping
# ----------------------------
country_index_map = {
    "japan": ("Tokyo Stock Exchange", "^N225"),
    "india": ("National Stock Exchange (NSE)", "^NSEI"),
    "us": ("NYSE / S&P 500", "^GSPC"),
    "usa": ("NYSE / S&P 500", "^GSPC"),
    "uk": ("London Stock Exchange", "^FTSE"),
    "china": ("Shanghai Stock Exchange", "000001.SS"),
    "south korea": ("Korea Exchange (KRX)", "^KS11")
}

# ----------------------------
# Exchange Rate Function
# ----------------------------
def get_exchange_rate(base_currency: str):
    url = f"https://api.exchangerate-api.com/v4/latest/{base_currency}"
    response = requests.get(url).json()

    return {
        "USD": response["rates"]["USD"],
        "INR": response["rates"]["INR"],
        "GBP": response["rates"]["GBP"],
        "EUR": response["rates"]["EUR"],
    }

# ----------------------------
# Stock Index Function
# ----------------------------
def get_index_value(symbol: str):
    ticker = yf.Ticker(symbol)
    data = ticker.history(period="1d")

    if data.empty:
        return "No data found"

    return float(data["Close"].iloc[-1])

# ----------------------------
# Main Agent Logic
# ----------------------------
def get_country_financial_data(country_name: str):
    country = country_name.lower()

    if country not in country_currency_map:
        return "Country not supported."

    currency = country_currency_map[country]
    exchange = get_exchange_rate(currency)

    stock_exchange_name, symbol = country_index_map[country]
    index_value = get_index_value(symbol)

    return {
        "country": country_name.title(),
        "currency": currency,
        "exchange_rates": exchange,
        "stock_exchange": stock_exchange_name,
        "index_symbol": symbol,
        "index_value": index_value
    }

# ----------------------------
# Manual Test
# ----------------------------
if __name__ == "__main__":
    result = get_country_financial_data("Japan")
    print(result)
