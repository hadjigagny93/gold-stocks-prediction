from .ingest import ImportTask
from .models import *

class CurrentImportTask(ImportTask):
    def transfer(self):
        return 1
