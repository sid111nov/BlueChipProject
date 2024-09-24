import yfinance as yf

import os, json, pandas as pd, time, random, io
from djia_companies import DJIA_LIST
from mongo_connection import getconnection2collection


ticker_list = []
pwd = os.getcwd()

file_path = os.path.join(pwd,"config","api.json")
config_dict = {}

with open(file_path,'r') as f:
    config_dict = json.loads(f.read())

# print(config_dict["ALPHAV"]) 


income_connection = getconnection2collection("stockdata","cashflow")

for djia in DJIA_LIST:
    ticker_list.append(djia[0])
try: 

    for ticker in ticker_list:
        ticker_data = yf.Ticker(ticker)
        df = None
        print(f"starting {ticker}")
        income_json = None
        
        result = income_connection.find_one({"ticker":ticker})

        if result is None:
            income_stmt = ticker_data.get_cash_flow()
            income_stmt = income_stmt.to_json(orient="records")
            income_connection.insert_one({
                "ticker": ticker,
                "cashflow_stmt": income_stmt
            })
        else:
            income_json = result["cashflow_stmt"]
            df = pd.read_json(io.StringIO(income_json), orient="records")

        print(df)
        time.sleep(random.uniform(6,10))
except Exception as e:
    print(e)        
finally:
    income_connection.client.close()