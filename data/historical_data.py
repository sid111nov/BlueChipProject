import yfinance as yf
import os, time, random, json,io
import pandas as pd
from  djia_companies import DJIA_LIST
from mongo_connection import getconnection2collection
import datetime
from db_connection import get_db_connection



ticker_list = ['CSCO']
mongo_connection = getconnection2collection("stockdata","tickers")
db_connection = get_db_connection()
cursor = db_connection.cursor()

#code for companies in dow joens industrial average
# for djia in DJIA_LIST:
#     ticker_list.append(djia[0])



QUERY = " INSERT INTO historical_data (ticker, date, open, high, low, close, volume, dividends,stock_splits ) values (%s,%s,%s,%s,%s,%s,%s,%s,%s )"

try:
      
    for ticker in ticker_list:
        print(f"starting {ticker}")
        tuple_list = []
        result = mongo_connection.find_one({"ticker":ticker})
        ticker_data = None
        hist_10y = None
        if result is None:
            ticker_data = yf.Ticker(ticker)
            hist_10y = ticker_data.history(period="10y")
            hist_10y.reset_index(inplace=True)
            json_obj = hist_10y.to_json(orient="records")
            mongo_connection.insert_one({
                    "ticker": ticker,
                    "historical_data": json_obj,
                    
            })
        else:
            json_str = result['historical_data']
            hist_10y = pd.read_json(io.StringIO(json_str), orient="records")
              
              
        
        # hist_10y.insert(0,"ticker",ticker)
        # for i in hist_10y.itertuples(index=False):
                
        #         ticker, date, open_price, high_price, low_price, close_price, volume, dividends, stock_splits = i
        #         date = date.strftime("%Y-%m-%d")
        #         tuple_list.append((
        #              ticker,
        #             date,
        #             open_price,
        #             high_price,
        #             low_price,
        #             close_price,
        #             volume,
        #             dividends,
        #             stock_splits
        #              ))
               
        # cursor.executemany(QUERY,tuple_list)
        # db_connection.commit()
        time.sleep(random.uniform(5,10))
except Exception as e:
     print("error thrown ",e)        
finally:
    db_connection.close()
    mongo_connection.client.close()
             

