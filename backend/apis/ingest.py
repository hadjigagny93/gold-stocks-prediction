from .models import *
import datetime


class Import(type):
    def __call__(cls, import_task):
        if cls is ImportTask:
            if import_task['transfer_mode'] == 0: return BackImportTask(import_task)
            elif import_task['transfer_mode'] == 1: return CurrentImportTask(import_task)
            else:
                raise NotImplementedError("This transfer mode paradigm is not yet implemented.")
        return super().__call__(import_task)

class ImportTask(object, metaclass=Import):

    def __init__(self, import_task, **kwargs):
        self.transfer_mode = import_task.get('transfer_mode')
        self.current_datetime = datetime.datetime.now()
        self.period = None
        self.batch = import_task.get('batch')

    def aggregate(self):

        pass

    def sample_batch(self):
        if self.batch:
            # retrieve all the data
            sample = Back.objects.values('new_header', 'public_date')
            print(sample)
            return sample
        pass

    def transfer(self):
         raise NotImplementedError("This method has not been implemented yet")

from .back_import import BackImportTask
from .current_import import CurrentImportTask
