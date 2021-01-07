import os 
import hashlib
import requests
from selenium import webdriver
from datetime import datetime
import psycopg2
from .settings import (
    REPO_DIR, 
    CONFIG_PATH, 
    BROWSER_CONFIGS, 
    DATA_DIR,
    DATABASES
)
#from .browser_config import BROWSER_CONFIGS
#from db_settings import DATABASES




class GoldNewsRetriever:
    """https://www.investing.com/commodities/gold-news"""

    def __init__(self, base_url='https://www.investing.com/commodities/gold-news'):
        self.base_url = base_url

    def scrape(self, **kwargs):
        #DEFAULT_NEWS_PER_PAGE = 10
        chrome_driver_path = BROWSER_CONFIGS['CHROME_DRIVER']
        user_agent = BROWSER_CONFIGS['USER_AGENT']
        driver = webdriver.Chrome(chrome_driver_path)
        url = self.base_url
        current = True
        if 'page' in kwargs:
            current = False
            page = kwargs.get('page')
            url = os.path.join(url, str(page))
            headers = {'User-Agent': user_agent}
            response = requests.get(url=url, headers=headers)
            if len(response.history) == 1:
                raise Exception("No data retrieved")
        driver.get(url)
        titles = self.__get_titles(driver)
        dates = self.__get_dates(driver)
        sources = self.__get_sources(driver)
        hashes = [hashlib.md5(title.encode()).hexdigest() for title in titles]
        chronos = [datetime.now().strftime("%m/%d/%Y, %H:%M:%S")] * len(hashes)
        # write data in txt file
        #self.register(chronos, hashes, titles, sources, dates, current)
        self.register_db(chronos, hashes, titles, sources, dates, current)

    @staticmethod
    def __get_titles(driver, limit=10):
        return [s.text for s in driver.find_elements_by_class_name("title")[3:limit + 3]]

    @staticmethod
    def __get_dates(driver, limit=10):
        return [s.text for  s in driver.find_elements_by_xpath('.//span[@class = "date"]')[:limit]]

    @staticmethod
    def __get_sources(driver, limit=10):
        return [s.text for s in driver.find_elements_by_xpath('//span[contains(text(), "By")]')[:limit]]


    def register(
        self, 
        chronos, 
        hashes, 
        titles, 
        sources, 
        dates, 
        current=True):
        path = 'back.txt'
        if current:
            path = 'current.txt'
            last_news = self.get_last_news()
        with open(os.path.join(DATA_DIR, path), "a") as file:
            for info in zip(
                chronos, 
                hashes, 
                titles, 
                sources, 
                dates):
                if current:
                    current_hash = info[1]
                    if current_hash in last_news:
                        # this new is already registered in tables
                        continue 
                for s in info:
                    if s != info[-1]:
                        s += '|'
                        file.write(s)
                    else:
                        file.write(s)
                file.write('\n')

    def register_db(
        self, 
        chronos,
        hashes, 
        titles, 
        sources, 
        dates,
        current=True):
        """ connect to a postgres sql instance of our db and push data """
        
        sql_where_clause_request = """
        SELECT * 
        FROM old 
        WHERE header_hash = %s;
        """
        sql_insert_request = """
        INSERT INTO old 
        (
            header_hash, 
            scraping_date, 
            new_header, 
            source, 
            public_date
            ) 
        VALUES (%s, %s, %s, %s, %s);
        """
        if current:
            sql_where_clause_request = """
            SELECT * 
            FROM current 
            WHERE header_hash = %s;
            """
            sql_insert_request = """
            INSERT INTO current 
            (
                header_hash, 
                scraping_date, 
                new_header, 
                source, 
                public_date
            ) 
            VALUES (%s, %s, %s, %s, %s);"""
        try:
            params = DATABASES
            conn = psycopg2.connect(**params)
            cur = conn.cursor()
            for info in zip(
                chronos, 
                hashes, 
                titles, 
                sources, 
                dates):
                chrono, hash_new, title, source, date = info
                cur.execute(sql_where_clause_request, (hash_new,))
                if cur.fetchall() != []:
                    # we can now add a new header new
                    print('this hash is already registered')
                    continue
                # get a breaking new, process & store it in the database
                # convert datetime to timestamp
                # chrono = chrono.replace(',', '')
                # insert data
                source = source.replace('By', '')
                date = date.replace('-', '')
                cur.execute(sql_insert_request, (hash_new, chrono, title, source, date))
                conn.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)

        finally:
            if conn is not None:
                # close communication with the database
                conn.close()
    
    @staticmethod
    def get_last_news():
        PREVIOUS_SCRAPED_NEWS = 10
        path = 'current.txt'
        with open(os.path.join(DATA_DIR, path), "r") as file:
            tail = file.readlines()[-PREVIOUS_SCRAPED_NEWS:]
            return [x.split('|')[1] for x in tail]
        #return hashes

    def back_scrape(self, pagination=2):
        lower = 2
        upper = pagination + lower
        for page in range(lower, upper):
            self.scrape(page=page)
