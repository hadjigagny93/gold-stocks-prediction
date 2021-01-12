from .models import *
import datetime
import hashlib


#datetime.datetime.strftime(date, '%Y-%m-%d')
class ImportTask(object):

    def __init__(self, import_task, **kwargs):
        self.transfer_mode = import_task.get('transfer_mode')
        self.current_date = datetime.date.today()
        

    def transfer(self):
        if self.transfer_mode == "current":
            str_date = datetime.datetime.strftime(self.current_date, '%Y-%m-%d')
            stock = {"date": str_date}
            daily_news_headers = Current.objects.filter(public_date=str_date).values('new_header')
            big_new = str()
            for news in daily_news_headers:
                big_new += news.get('new_header')
            new_hash = hashlib.md5(big_new.encode()).hexdigest()
            # check if the hash is already in the db 
            news_header_exists = Stock.objects.filter(new_hash=new_hash)
            if news_header_exists:
                raise
            # push data to stock table
            stock = {**stock, **{"news": big_new, "new_hash": new_hash}}
            # call yfinance sdk 
            stock = {**stock, **{"price": 0}}
            stock_created = Stock.objects.create(**stock)
            if stock_created:
                stock_created_status = "upated"

            # create transfertask objects
            name = 'current'
            now = datetime.datetime.now()
            from_tab, created = Mode.objects.get_or_create(name=name)
            transfer_task_params = {
                'current_datetime': datetime.datetime.now(), 
                'from_tab': from_tab,
                'status': stock_created_status}
            register_created = TransferTask.objects.create(**transfer_task_params)


            