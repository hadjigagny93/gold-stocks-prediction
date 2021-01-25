import requests
from scraper import GoldNewsRetriever
import os 
from docker_env import is_dot_docker_env_there


def api_call(scraper="current", pagination=None):
    hosts = {
        True: 'host.docker.internal',
        False: 'localhost'
    }

    BASE_URL = f"http://{hosts[is_dot_docker_env_there()]}:8000/apis/88bvchvnsj7"
    url = os.path.join(BASE_URL, scraper)
    bot = GoldNewsRetriever()
    
    if scraper == "back":
        fresh_news = bot.back_scraper(pagination=pagination)
        request_return = requests.post(url, json=fresh_news)
        return 

    fresh_news = bot.current_scraper()
    request_return = requests.post(url, json=fresh_news)
