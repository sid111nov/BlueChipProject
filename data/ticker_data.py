import yfinance as yf
import sqlite3 
import io
from datetime import datetime,timedelta
import pandas as pd

conn = sqlite3.Connection('stick_data.db', timeout=10)
cursor = conn.cursor()

cursor.execute(
  '''  create table if not exists stock_cache (
  ticker TEXT PRIMARY KEY,
  data TEXT,
  last_update TIMESTAMP  
  )
  '''
)

def getTickerData(ticker:str):
    ticker_data = yf.Ticker(ticker).history(period='5d').to_csv()
    return ticker_data

def save_ticker_data(ticker,data):
    now = datetime.now()
    cursor.execute(
        '''
    insert or replace into stock_cache (ticker,data,last_update)  values (?,?,?)
    ''',(ticker,data,now)
    )
    conn.commit()

def get_cached_data(ticker:str):
    cursor.execute(
        '''
        select data,last_update from stock_cache where ticker = ?
    ''',(ticker,)
    )    
    result = cursor.fetchone()

    if result:
        data,last_update = result
        last_update = datetime.strptime(last_update,"%Y-%m-%d %H:%M:%S.%f")
        if(datetime.now() - last_update < timedelta(hours=4)):
            return pd.read_csv(io.StringIO(data))
    return None    

def get_stock_data(ticker:str):
    cached_data = get_cached_data(ticker)
    if cached_data is not None:
        return cached_data
    
    else:
        data = getTickerData(ticker)
        save_ticker_data(ticker,data)
        return pd.read_csv(io.StringIO(data))


mcd_data = get_stock_data("MCD")

ixic_data = get_stock_data("^IXIC")

dji_data = get_stock_data("^DJI")

def getAggregateDataFrame():

    global mcd_data, ixic_data, dji_data

    mcd_copy = mcd_data.copy()
    ixic_copy = ixic_data.copy()
    dji_copy = dji_data.copy()

    mcd_copy = mcd_copy.drop(columns=["Open","High","Low","Stock Splits"])
    ixic_copy = ixic_copy.drop(columns=["Open","High","Low","Volume","Dividends","Stock Splits"])
    dji_copy = dji_copy.drop(columns=["Open","High","Low","Volume","Dividends","Stock Splits"])

    mcd_copy = pd.merge(mcd_copy,ixic_copy,on='Date')
    mcd_copy = pd.merge(mcd_copy,dji_copy,on='Date')
    mcd_copy.rename(columns={'Close_x':'MCD_Share_Price_Close','Volume':'Volume_Traded','Close_y':'NASDAQ_Composite','Close':'Dow_Jones_Ind_Avg'},inplace=True)
    mcd_copy['Date'] = pd.to_datetime(mcd_copy['Date'])
    mcd_copy['Date'] = mcd_copy['Date'].dt.strftime('%Y-%m-%d')
    return mcd_copy