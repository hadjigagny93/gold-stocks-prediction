from scraper import GoldNewsRetriever
import os 
from settings import DATA_DIR

class Register:

    def __init__(self, scraper="current", pagination=None):
        bot = GoldNewsRetriever()
        chronos = []
        hashes = []
        titles = []
        sources = []
        dates = []
        if scraper == "current":
            self.current = True
            fresh_news = bot.current_scraper()
        elif scraper == "back":
            self.current = False
            fresh_news = bot.back_scraper(pagination=pagination)
        else:
            raise Exception("out")
        for data in fresh_news:
            chronos.append(data.get('scraping_date'))
            hashes.append(data.get('header_hash'))
            titles.append(data.get('new_header'))
            sources.append(data.get('source'))
            dates.append(data.get('public_date'))
            self.data = chronos, hashes, titles, sources, dates
            
    def register(self):
        chronos, hashes, titles, sources, dates = self.data
        current = self.current
        file_name = 'back.txt'
        if current:
            file_name = 'current.txt'
            last_news = self.get_last_news(file_name)
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
                        print("already in file")
                        continue
                for s in info:
                    if s != info[-1]:
                        s += '|'
                        file.write(s)
                    else:
                        file.write(s)
                file.write('\n')
    
    def get_last_news(self, file_name):
        PREVIOUS_SCRAPED_NEWS = 10
        file_path = self.__check_file(file_name)
        with open(file_path, "r") as file:
            tail = file.readlines()[-PREVIOUS_SCRAPED_NEWS:]
            return [x.split('|')[1] for x in tail]

    @staticmethod
    def __check_file(file_name):
        file_path = os.path.join(DATA_DIR, file_name)
        if not os.path.exists(file_path):
            # create that file
            shell_touch = f"touch {file_path}"
            os.system(shell_touch)
        return file_path

    '''
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
    '''


      