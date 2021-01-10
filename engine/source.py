# import file
# !pip install yfinance
import yfinance as yf
import datetime
import os
import pandas as pd
#data = pd.read_csv("/content/data.txt", sep="|", names=["date", "hash", "text", "source", "Date"])

def normalize_date(s, start_date="2020-12-14"):
  month = {
    "Aug": "08",
    "Dec": "12",
    "Jul": "07",
    "Nov": "11",
    "Oct": "10",
    "Sep": "09"
    }
  if "hours" in s:
    return  datetime.datetime.strptime(start_date, '%Y-%m-%d')
  date_list_format = s.replace("-", "").replace(",", "").split(' ')[2:]
  date_list_format[0] = month[date_list_format[0]]
  m, d, y = date_list_format
  date_list_format = [y, m, d]
  s = "-".join(date_list_format)
  return datetime.datetime.strptime(s, '%Y-%m-%d')

def get_news(file_path):
  df = pd.read_csv(file_path, sep="|", names=["date", "hash", "text", "source", "Date"])
  df = df[["text", "Date"]]
  df.text = df.text.apply(lambda s: s + " ")
  df.Date = df.Date.apply(normalize_date)
  df = df.groupby('Date')['text'].sum().reset_index()
  return df

def get_price(stock="GLD", start_date="2020-07-23", end_date="2020-12-14"):
  df = yf.download("GLD", start=start_date, end=end_date)
  df = df.reset_index()[["Date", "Close"]]
  # df.Date = df.Date.apply(lambda s: s.strftime('%Y-%m-%d'))
  # df.Close = df.Close.fillna()
  return df

def aggregate_data(news_df, price_df):
  df = news_df.join(price_df.set_index('Date'), on='Date')
  df.Close = df.Close.fillna(df.Close.mean())
  return df

def generate_df(
    start_date_news,
    source="os",
    file_path="/content/data.txt",
    stock="GLD",
    start_date_stock="2020-07-23",
    end_date_stock="2020-12-14"):
  if source == "os":
    news = get_news(file_path)
  price = get_price(stock=stock, start_date=start_date_stock, end_date=end_date_stock)
  df = aggregate_data(news, price)
  return df
