import alpha_vantage as av
from alpha_vantage.fundamentaldata import FundamentalData
import os, json, pandas as pd, time, random
from djia_companies import DJIA_LIST
from mongo_connection import getconnection2collection


ticker_list = []
pwd = os.getcwd()

file_path = os.path.join(pwd,"config","api.json")
config_dict = {}

with open(file_path,'r') as f:
    config_dict = json.loads(f.read())

print(config_dict["ALPHAV"]) 

fd  = FundamentalData(key=config_dict["ALPHAV"],output_format='pandas')
income_connection = getconnection2collection("stockdata","income_statement")

for djia in DJIA_LIST:
    ticker_list.append(djia[0])
try: 

    for ticker in ticker_list:
        print(f"starting {ticker}")
        income_json = None
        income_stmt,_ = fd.get_income_statement_annual(symbol=ticker)
        result = income_connection.find_one({"ticker":ticker})

        if result is None:
            income_stmt = income_stmt.to_json(orient="records")
            income_connection.insert_one({
                "ticker": ticker,
                "income_stmt": income_stmt
            })
        else:
            income_json = result["income_stmt"]

        time.sleep(random.uniform(6,10))
except Exception as e:
    print(e)        
finally:
    income_connection.client.close()