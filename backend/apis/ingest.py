from .models import *
import datetime
import hashlib
from django.db.models import Sum
from django.db.models.functions import Cast
from django.db.models import FloatField


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
            price = self.get_stock_price(str_date)
            stock = {**stock, **{"price": price}}
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
        else:
            #City.objects.values('country__name').annotate(Sum('population'))
            str_date = datetime.datetime.strftime(self.current_date, '%Y-%m-%d')
            daily_news_headers = self.aggregate_data(Back.objects.values('public_date', 'new_header')[::1])
            #print(daily_news_headers[0])
            updated_news = []
            for data in daily_news_headers:
                date = data['date']
                price = self.get_stock_price(date)
                new_hash = hashlib.md5(data['news'].encode()).hexdigest()
                data = {**data, **{"price": price, 'new_hash': new_hash}}
                updated_news.append(data)
            for stock in updated_news:
                stock_created = Stock.objects.create(**stock)
                        # create transfertask objects
            name = 'back'
            now = datetime.datetime.now()
            from_tab, created = Mode.objects.get_or_create(name=name)
            transfer_task_params = {
                'current_datetime': datetime.datetime.now(), 
                'from_tab': from_tab,
                'status': 'created'}
            register_created = TransferTask.objects.create(**transfer_task_params)

        
    @staticmethod
    def get_stock_price(s):
        return 0

    @staticmethod
    def aggregate_data(s):
        dates = list(set([d['public_date'] for d in s]))
        #return dates
        r = {}
        for date in dates:
            r[date] = ''
            for d in s:
                dd = d['public_date']
                nn = d['new_header']
                if dd == date:
                    r[date] += nn + ' '
        return_format = []
        for s in r:
            d = {}
            d['date'] = s
            d['news'] = r[s]
            return_format.append(d)
        return return_format








            