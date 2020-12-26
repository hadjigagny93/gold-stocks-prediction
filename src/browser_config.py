import os

BROWSER_CONFIGS = {
    'CHROME_DRIVER': os.getenv('CHROME_DRIVER_PATH'),
    'USER_AGENT': os.getenv('USER_AGENT')
}
