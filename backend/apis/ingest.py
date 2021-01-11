

class Import(type):
    def __call__(cls, import_task):
        if cls is ImportTask:
            if import_task['transfer_mode'] == 0: return BackImportTask(import_task)
            elif import_task['transfer_mode'] == 1: return BackImportTask(import_task)
            else:
                raise NotImplementedError("This autoML paradigm is not yet implemented.")
        return super().__call__(automl_import_task)

class ImportTask(object, metaclass=Import):

    def __init__(self, import_task, **kwargs):
        self.transfer_mode = import_task.get('transfer_mode')

     def transfer(self):
         raise NotImplementedError("This method has not been implemented yet")

from back_import import BackImportTask
from unsupervised import CurrentImportTask
