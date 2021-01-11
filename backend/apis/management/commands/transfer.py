from django.core.management.base import BaseCommand
from apis.ingest import ImportTask

class Command(BaseCommand):
    help = 'run scripts for transfer data from current to apis_current & apis_back to stock'

    def add_arguments(self, parser):
        parser.add_argument('mode', type=int)

    def handle(self, *args, **kwargs):
        transfer_mode = kwargs.get('mode')
        import_task = {"transfer_mode": transfer_mode}
        import_task_instance = ImportTask(import_task)
        print(import_task_instance.transfer())
