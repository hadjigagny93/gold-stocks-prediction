from .ingest import ImportTask
from .models import *

class BackImportTask(ImportTask):
    def transfer(self):
        return 1
