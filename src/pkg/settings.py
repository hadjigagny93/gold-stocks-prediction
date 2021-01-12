import os

# DEFAULT DIRS
REPO_DIR = os.path.abspath(os.path.join(os.path.join(os.path.dirname(__file__), '..'), '..'))
CONFIG_PATH = os.path.join(REPO_DIR, 'config/browser.yaml')
DATA_DIR = os.path.join(REPO_DIR, 'data/news')


# DATABASE SETTINGS
#DATABASES = {
#        'database': os.getenv("DB_NAME"),
#        'user': os.getenv("DB_USER"),
#        'password': os.getenv("DB_PASSWORD"),
#        'host': os.getenv("DB_HOST"),
#        'port': os.getenv("DB_PORT"),
#}

# BROWSER CONFIGS
#BROWSER_CONFIGS = {
#    'CHROME_DRIVER': os.getenv('CHROME_DRIVER_PATH'),
#    'USER_AGENT': os.getenv('USER_AGENT')
#}


# BASE URL
BASE_URL = "https://www.investing.com/commodities/gold-news"

# REGISTER MODE
PERMITTED_REGISTER_MODE = ("api", "fs")
