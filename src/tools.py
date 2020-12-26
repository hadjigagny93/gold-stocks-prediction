from datetime import datetime

def datetime_to_timestamp(s):
    datetime_object = datetime.strptime(s, '%m/%d/%Y %H:%M:%S')
    timestamp = datetime.timestamp(datetime_object)
    return timestamp
