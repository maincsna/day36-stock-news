import requests
from twilio.rest import Client

VIRTUAL_TWILIO_NUMBER = "+16822973785"
VERIFIED_NUMBER = "+13107458919"

STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

    ## STEP 1: Use https://www.alphavantage.co/documentation/#daily
# When stock price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").

STOCK_API_KEY = "X3Y96TJPZXWQ5I1I"
NEWS_API_KEY = "aff73b7fbb50404d80b56d97242485eb"
TWILIO_SID = "AC94b6688c7cdc5e893b5a971c65682e14"
TWILIO_AUTH_TOKEN = "26e321457f0cae89a02f9c0c71c37fc3"

# 1. - Get yesterday's closing stock price. Hint: You can perform list comprehensions on Python dictionaries. e.g. [new_value for (key, value) in dictionary.items()]
stock_params ={
    "function": "TIME_SERIES_DAILY_ADJUSTED",
    "symbol": STOCK_NAME,
    "apikey": STOCK_API_KEY,
}

response = requests.get(STOCK_ENDPOINT,params=stock_params)
data = response.json()["Time Series (Daily)"]
data_list = [value for (key,value) in data.items()]
yesterday_data = data_list[0]
yesterday_closing_price = yesterday_data["4. close"]
print(yesterday_closing_price)

#2. - Get the day before yesterday's closing stock price
day_before_yesterday_data = data_list[1]
day_before_yesterday_closing_price = day_before_yesterday_data["4. close"]
print(day_before_yesterday_closing_price)

#3. - Find the positive difference between 1 and 2. e.g. 40 - 20 = -20, but the positive difference is 20. Hint: https://www.w3schools.com/python/ref_func_abs.asp
difference = float(yesterday_closing_price) - float(day_before_yesterday_closing_price)
up_down = None
if difference > 0:
    up_down = "🔺"
else:
    up_down = "🔻️"

#4. - Work out the percentage difference in price between closing price yesterday and closing price the day before yesterday.
diff_percent = (difference/float(yesterday_closing_price)) * 100
print(diff_percent)

#5. - If TODO4 percentage is greater than 5 then print("Get News").

#6. - Instead of printing ("Get News"), use the News API to get articles related to the COMPANY_NAME.
if abs(diff_percent) > 1:
    news_params = {
        "apikey": NEWS_API_KEY,
        "qInTitle": COMPANY_NAME,
    }
    news_response = requests.get(NEWS_ENDPOINT,params=news_params)
    articles = news_response.json()["articles"]

#7. - Use Python slice operator to create a list that contains the first 3 articles. Hint: https://stackoverflow.com/questions/509211/understanding-slice-notation
three_articles = articles[:3]
print(three_articles)

## STEP 3: Use twilio.com/docs/sms/quickstart/python
    #to send a separate message with each article's title and description to your phone number. 

#8. - Create a new list of the first 3 article's headline and description using list comprehension.
formatted_articles = [f"{STOCK_NAME}:{up_down}{diff_percent}%\nHeadline:{article['title']}.\nBrief:{article['description']}" for article in three_articles]
print(formatted_articles)

#9. - Send each article as a separate message via Twilio.
client = Client(TWILIO_SID,TWILIO_AUTH_TOKEN)


#Optional : Format the message like this:
for article in formatted_articles:
    message = client.messages.create(
        body = article,
        from_=VIRTUAL_TWILIO_NUMBER,
        to=VERIFIED_NUMBER,
    )
