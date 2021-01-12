import os
import hashlib
import requests
from selenium import webdriver
from datetime import datetime
import psycopg2
from settings import (
    REPO_DIR,
    CONFIG_PATH,
    DATA_DIR,
    #DATABASES,
    BASE_URL,
    #PERMITTED_REGISTER_MODE,
)
from exceptions import (
    RegisterModeException,
    EmptyNewsPageException,
)
from docker_env import is_dot_docker_env_there
import yaml


class GoldNewsRetriever:

    def __init__(self):
        self.base_url = BASE_URL

    @staticmethod
    def load_configs():
        docker_env = is_dot_docker_env_there()
        if docker_env:
            # there, that's in docker env
            from chrome import set_chrome_options
            options = set_chrome_options()
            return options
        with open(os.path.join(REPO_DIR, "config/browser.yaml")) as file:
            file_content = yaml.full_load(file)
            BROWSER_CONFIGS = file_content["NAVIGATOR_SETTINGS"]
            chrome_driver_path = BROWSER_CONFIGS['CHROME_DRIVER']
            user_agent = BROWSER_CONFIGS['USER_AGENT']
        return chrome_driver_path, user_agent

    def scrape(self, **kwargs):
        configs = self.load_configs()
        if isinstance(configs, tuple):
            # local env dev
            chrome_driver_path, user_agent = configs
            driver = webdriver.Chrome(chrome_driver_path)
        else:
            # docker env deployment
            options = configs
            driver = webdriver.Chrome(options=options)

        url = self.base_url
        current = True
        if 'page' in kwargs:
            current = False
            page = kwargs.get('page')
            url = os.path.join(url, str(page))
            docker_env = is_dot_docker_env_there()
            if docker_env:
                response = requests.get(url=url)
            else:
                headers = {'User-Agent': user_agent}
                response = requests.get(url=url, headers=headers)
            if len(response.history) == 1:
                #raise Exception("No data retrieved")
                raise EmptyNewsPageException(page)
        driver.get(url)
        titles = self.__get_titles(driver)
        dates = self.__get_dates(driver)
        sources = self.__get_sources(driver)
        hashes = [hashlib.md5(title.encode()).hexdigest() for title in titles]
        chronos = [datetime.now().strftime("%m/%d/%Y, %H:%M:%S")] * len(hashes)
        # write data in txt file
        """
        if self.register_mode == "FS":
            self.register(chronos, hashes, titles, sources, dates, current)
            return
        self.register_db(chronos, hashes, titles, sources, dates, current)
        """
        # return data as dict
        scraped_data = []
        for data in zip(
            hashes,
            chronos,
            titles,
            sources,
            dates):
            s = dict()
            s['header_hash'], s['scraping_date'], s['new_header'], s['source'], s['public_date'] = data
            scraped_data.append(s)
        return scraped_data

    def current_scraper(self):
        return self.scrape()

    def back_scraper(self, pagination):
        lower = 2
        upper = pagination + lower
        history_data = []
        for page in range(lower, upper):
            print(page)
            history_data += self.scrape(page=page)
            print("ok")
        return history_data


    @staticmethod
    def __get_titles(driver, limit=10):
        return [s.text for s in driver.find_elements_by_class_name("title")[3:limit + 3]]

    @staticmethod
    def __get_dates(driver, limit=10):
        return [s.text for  s in driver.find_elements_by_xpath('.//span[@class = "date"]')[:limit]]

    @staticmethod
    def __get_sources(driver, limit=10):
        return [s.text for s in driver.find_elements_by_xpath('//span[contains(text(), "By")]')[:limit]]
    
    #def back_scrape(self, pagination=2):
    #    lower = 2
    #    upper = pagination + lower
    #    for page in range(lower, upper):
    #        print(page)
    #        self.scrape(page=page)
    #        print("ok")
    
"""
if __name__ == "__main__":
    instance = GoldNewsRetriever(register_mode="api")
    print(instance.scrape())
"""
