import fredapi as fred
import pandas as pd, time, random, os, json, traceback, io
from mongo_connection import getconnection2collection
from db_connection import get_db_connection
import datetime


# ###
# Consumer Price Index (CPI)	CPIAUCSL
# Federal Funds Rate	FEDFUNDS
# Real Gross Domestic Product	GDPC1
# Unemployment Rate	UNRATE
# 10-Year Treasury Yield	DGS10
# U.S. Dollar Index	DTWEXM
# Producer Price Index (PPI)	PPIACO
# Industrial Production	INDPRO
# Crude Oil Prices (WTI)	DCOILWTICO

# ###

mongo_connection = getconnection2collection("stockdata","macro")
db_connection = get_db_connection()
pwd = os.getcwd()

file_path = os.path.join(pwd,"config","api.json")
api_json = None

with open(file_path,'r') as f:
    api_json=json.loads(f.read())


fa = fred.Fred(api_key=api_json["FRED"])

def getseriesidsformacrodata():
    id_list = ['FEDFUNDS','CPIAUCSL','GDP','UNRATE','M2sL','INDPRO','UMCSENT','DCOILWTICO','RSAFS','DGS10']
    return id_list

id_list = getseriesidsformacrodata()

try:
     
    for id in id_list:
        

            print(f"Geting data {id}")
            series = None
            json_str = None
            series_df = None
            result = mongo_connection.find_one({"macro":id})
            if result is None:
                series = fa.get_series(id)
                
                mongo_connection.insert_one({
                    "macro":id,
                    "series":series.to_json()
                })
            else:
                json_str = result["series"]
                series_data = json.loads(json_str)


            series_df = pd.DataFrame(list(series_data.items()),columns=["date","value"])
            series_df['date'] = pd.to_datetime(series_df['date'],unit='ms')
            series_df['date'] = series_df['date'].dt.strftime("%Y-%m-%d")
            # print(series_df)

            time.sleep(random.uniform(3,10))



except Exception as e:
    stacktrace = traceback.format_exc()
    print(f"Exception thrown at {id} with {stacktrace}")

finally:
     
    db_connection.close()
    mongo_connection.client.close()



