import streamlit as st
import data.ticker_data as td
import pandas as pd
import warnings, os, pickle
from datetime import datetime
import prophet



st.title("McDonalds Stock Price Predictor")

st.write("**Note**: This is **not a financial advice**, this is simply a **demo** app on timeseries forecasting")

col1, col2 = st.columns(2)

last_known_price = None
last_known_volume = None
dividends = 0
dow_jones = None
nasdaq_composits = None

df = td.getAggregateDataFrame()

cwd = os.getcwd()

model_7days = None
model_30days = None


with col1:
    last_known_price = st.number_input(label="Enter last known/closing Price",min_value=0)
    dividends = st.number_input(label="Enter Dividend",min_value=0)

with col2:
    last_known_volume = st.number_input(label="Enter last known/closing Volume",min_value=0)
    nasdaq_composits = st.number_input(label="Enter Nasdaq Composit",min_value=0)
    dow_jones = st.number_input(label="Enter Dow Jones Industrial Average",min_value=0)
    

with open(os.path.join(cwd,"artifacts","prophet_model_7days.pkl"),'rb') as f:
    model_7days = pickle.load(f)

with open(os.path.join(cwd,"artifacts","prophet_model_30_days.pkl"),'rb') as f:
    model_30days = pickle.load(f)

input_list=[datetime.now(),last_known_price,last_known_volume,dividends,nasdaq_composits,dow_jones]
input_df = pd.DataFrame([input_list],columns=['ds','MCD_Close','MCD_Volume','MCD_Dividends','^IXIC_Close','^DJI_Close'])

if df.empty:
    st.error("Cached data is empty or invalid!")
else:
    st.dataframe(df)
    
    
if(st.button("Submit",type='primary')):
    columns_to_check = ['MCD_Close', 'MCD_Volume', '^IXIC_Close', '^DJI_Close']

    if(input_df[columns_to_check].isnull().values.any() or (input_df[columns_to_check]==0).values.any()):
        st.error(f"Error: Missing or zero values found in required columns {columns_to_check}")
    
    else:
        price_1 = model_7days.predict(input_df)
        price_2 = model_30days.predict(input_df)
        price_1_list = price_1[['yhat','yhat_lower','yhat_upper']].values.tolist()[0]
        price_2_list = price_2[['yhat','yhat_lower','yhat_upper']].values.tolist()[0]

        st.header(f"Price Prediction for next **7 Days**: :red[{round(price_1_list[0],2)}]")
        st.subheader(f"lower range: :blue[{round(price_1_list[1],2)}] upper range: :blue[{round(price_1_list[2],2)}]")

        st.header(f"Price Prediction for next **30 Days**: :red[{round(price_2_list[0],2)}]")
        st.subheader(f"lower range: :blue[{round(price_2_list[1],2)}] upper range: :blue[{round(price_2_list[2],2)}]")

    