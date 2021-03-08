import requests
from scraper import GoldNewsRetriever
import os 
from docker_env import is_dot_docker_env_there


def api_call(scraper="current", pagination=None):
    host_context = 'localhost'
    if is_dot_docker_env_there():
        host_context = 'host.docker.internal'

    url = os.path.join(f"http://{host_context}:8000/apis/88bvchvnsj7", scraper)
    bot = GoldNewsRetriever()
    
    if scraper == "back":
        fresh_news = bot.back_scraper(pagination=pagination)
        request_return = requests.post(url, json=fresh_news)
        return 

    fresh_news = bot.current_scraper()
    request_return = requests.post(url, json=fresh_news)
