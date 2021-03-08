import datetime

def normalize_date(s):
  month = {
    "Jan": "01",
    "Feb": "02",
    "Aug": "08",
    "Dec": "12",
    "Jul": "07",
    "Nov": "11",
    "Oct": "10",
    "Sep": "09"
    }
  if "ago" in s:
    #return  datetime.datetime.strptime(start_date, '%Y-%m-%d')
    date = datetime.date.today()
    return datetime.datetime.strftime(date, '%Y-%m-%d')
  date_list_format = s.replace("-", "").replace(",", "").split(' ')[2:]
  date_list_format[0] = month[date_list_format[0]]
  m, d, y = date_list_format
  date_list_format = [y, m, d]
  s = "-".join(date_list_format)
  return s 
