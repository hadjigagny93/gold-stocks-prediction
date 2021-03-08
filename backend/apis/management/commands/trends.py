from django.core.management.base import BaseCommand
from apis.forecast import Forecast

class Command(BaseCommand):
    help = 'get predictions'

    """
    def add_arguments(self, parser):
        parser.add_argument('mode', type=str)
    """

    def handle(self, *args, **kwargs):
        #transfer_mode = kwargs.get('mode')
        #import_task = {
        #    "transfer_mode": transfer_mode,
        #    }
        #import_task_instance = ImportTask(import_task)
        #import_task_instance.transfer()
        static_url = "http://0.0.0.0:5000"
        Forecast(base_url=static_url).get_predictions()

