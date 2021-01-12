import requests
from scraper import GoldNewsRetriever
import os 


def api_call(scraper="current", pagination=None):
    BASE_URL = "http://127.0.0.1:8000/apis/88bvchvnsj7"
    url = os.path.join(BASE_URL, scraper)
    bot = GoldNewsRetriever()
    
    if scraper == "back":
        fresh_news = bot.back_scraper(pagination=pagination)
        request_return = requests.post(url, json=fresh_news)
        return 

    fresh_news = bot.current_scraper()
    request_return = requests.post(url, json=fresh_news)

