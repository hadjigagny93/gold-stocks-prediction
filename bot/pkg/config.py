
from settings import REPO_DIR
from docker_env import is_dot_docker_env_there
from selenium import webdriver
import os
import yaml 

def load_configs():
    docker_env = is_dot_docker_env_there()
    if docker_env:
        # there, that's in docker env
        from chrome import set_chrome_options
        options = set_chrome_options()
        return options
    with open(os.path.join(REPO_DIR, "config/browser.yaml")) as file:
        file_content = yaml.full_load(file)
        browser_config = file_content["NAVIGATOR_SETTINGS"]
        chrome_driver_path = browser_config['CHROME_DRIVER']
        user_agent = browser_config['USER_AGENT']
    return chrome_driver_path, user_agent

def get_driver():
    configs = load_configs()
    if isinstance(configs, tuple):
        # local env dev
        chrome_driver_path, user_agent = configs
        driver = webdriver.Chrome(chrome_driver_path)
        return driver, user_agent
    # docker env deployment
    user_agent = None
    options = configs
    driver = webdriver.Chrome(options=options)
    return driver, user_agent