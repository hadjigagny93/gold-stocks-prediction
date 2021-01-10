# import file
# !pip install yfinance
import yfinance as yf
import datetime
import os
import pandas as pd
from tools import normalize_date
from constants import *
from datetime import datetime

def get_news_from_db(conn_params):
    pass

def get_news(file_path):
  df = pd.read_csv(file_path, sep="|", names=NAMES)
  df = df[MODELS_NAMES]
  df.Text = df.Text.apply(lambda s: s + " ")
  df.Date = df.Date.apply(normalize_date)
  df = df.groupby('Date')['Text'].sum().reset_index()
  return df

def get_price(stock="GLD", start_date="2020-07-23", end_date="2020-12-14"):
  df = yf.download("GLD", start=start_date, end=end_date)
  df = df.reset_index()[STOCK_NAMES]
  return df

def aggregate_data(news_df, price_df):
  df = news_df.join(price_df.set_index('Date'), on='Date')
  df.Close = df.Close.fillna(df.Close.mean())
  return df

def generate_df(
    source,
    file_path,
    stock="GLD",
    start_date_stock="2020-07-23",
    end_date_stock="2020-12-14"):
  if source == "os":
      news = get_news(file_path)
  else:
      # connect to database and retrieve data
      pass
  price = get_price(stock=stock, start_date=start_date_stock, end_date=end_date_stock)
  df = aggregate_data(news, price)
  return df
