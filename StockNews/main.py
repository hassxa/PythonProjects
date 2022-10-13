import requests
from datetime import date, timedelta
from twilio.rest import Client
import html

STOCK = "AAPL"
COMPANY_NAME = "Apple Inc"
URL_STOCKS = "https://www.alphavantage.co/query?"
API_KEY_STOCKS = "# Your api key stocks"
URL_NEWS = "https://newsapi.org/v2/everything?"
API_KEY_NEWS = "# Your api key news"

ACCOUNT_SID = "# Your account id in Twilio"
AUTH_TOKEN = "# Your authorization token in Twilio"
TWILIO_PHONE_NUMBER = "# Your phone number in Twilio"


def get_date(days):
    date_to_get = date.today() - timedelta(days=days)
    return date_to_get


def request_data(url, params):
    response = requests.get(url=url, params=params)
    data = response.json()
    return data


# Get dates
yesterday = get_date(1)
day_before_yesterday = get_date(2)

parameters = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK,
    "apikey": API_KEY_STOCKS
}

# Working with Stock Api
stock_data = request_data(URL_STOCKS, parameters)
daily_price = stock_data["Time Series (Daily)"]
yesterday_close = daily_price[f"{yesterday}"]["4. close"]
day_before_yesterday_close = daily_price[f"{day_before_yesterday}"]["4. close"]

# Calculate price change between yesterday and day before yesterday
price_change = round(((float(yesterday_close) / float(day_before_yesterday_close)) - 1) * 100, 2)

# Working with News Api
parameters = {
    "q": COMPANY_NAME,
    "from": f"{yesterday}",
    "apiKey": API_KEY_NEWS
}
response_news = requests.get(url=URL_NEWS, params=parameters)
data_news = response_news.json()
first_three_news = data_news["articles"][:3]

# Sending message
if price_change >= 5 or price_change <= 5:
    client = Client(ACCOUNT_SID, AUTH_TOKEN)
    symbol = "🔺" if price_change >= 5 else "🔻"
    header = f"{STOCK}: {symbol}{price_change}%"
    for index in range(len(first_three_news)):
        title = html.unescape(first_three_news[index]["title"])
        description = html.unescape(first_three_news[index]["description"])
        message = client.messages \
            .create(
                body=f"{header}\n\n{title}\n\n{description}",
                from_=TWILIO_PHONE_NUMBER,
                to='# Your phone number'
            )
        print(message.status)
