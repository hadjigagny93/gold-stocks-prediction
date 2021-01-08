import os
import hashlib
import requests
from selenium import webdriver
from datetime import datetime
import psycopg2
from settings import (
    REPO_DIR,
    CONFIG_PATH,
    #BROWSER_CONFIGS,
    DATA_DIR,
    DATABASES,
    BASE_URL,
    PERMITTED_REGISTER_MODE,
)
from exceptions import (
    RegisterModeException,
    EmptyNewsPageException,
)
import yaml



class GoldNewsRetriever:

    def __init__(self, register_mode="FS"):
        self.base_url = BASE_URL
        if register_mode not in PERMITTED_REGISTER_MODE:
            raise RegisterModeException(register_mode)
        self.register_mode = register_mode

    def scrape(self, **kwargs):
        with open(os.path.join(REPO_DIR, "config/browser.yaml")) as file:
            file_content = yaml.full_load(file)
            try:
                BROWSER_CONFIGS = file_content["NAVIGATOR_SETTINGS"]
            except KeyError:
                raise
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
                #raise Exception("No data retrieved")
                raise EmptyNewsPageException(page)
        driver.get(url)
        titles = self.__get_titles(driver)
        dates = self.__get_dates(driver)
        sources = self.__get_sources(driver)
        hashes = [hashlib.md5(title.encode()).hexdigest() for title in titles]
        chronos = [datetime.now().strftime("%m/%d/%Y, %H:%M:%S")] * len(hashes)
        # write data in txt file
        if self.register_mode == "FS":
            self.register(chronos, hashes, titles, sources, dates, current)
            return
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

    @staticmethod
    def __check_file(file_name):
        file_path = os.path.join(DATA_DIR, file_name)
        if not os.path.exists(file_path):
            # craete taht file
            shell_touch = f"touch {file_path}"
            os.system(shell_touch)
        return file_path

    def register(
        self,
        chronos,
        hashes,
        titles,
        sources,
        dates,
        current=True):
        file_name = 'back.txt'
        if current:
            file_name = 'current.txt'
            last_news = self.get_last_news(file_name)
        #file_path = os.path.join(DATA_DIR, file_name)
        # if not os.path.exists(file_path):
        #    create that file
        #    shell_touch = f"touch {file_path}"
        #    os.system(shell_touch)
        file_path = self.__check_file(file_name)

        with open(file_path, "a") as file:
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

    def get_last_news(self, file_name):
        PREVIOUS_SCRAPED_NEWS = 10
        #file_name = 'current.txt'
        #file_path = os.path.join(DATA_DIR, file_name)
        #if not os.path.exists(file_path):
        #    create taht file
        #    shell_touch = f"touch {file_path}"
        #    os.system(shell_touch)
        file_path = self.__check_file(file_name)
        with open(file_path, "r") as file:
            tail = file.readlines()[-PREVIOUS_SCRAPED_NEWS:]
            return [x.split('|')[1] for x in tail]
        #return hashes

    def back_scrape(self, pagination=2):
        lower = 2
        upper = pagination + lower
        for page in range(lower, upper):
            self.scrape(page=page)
