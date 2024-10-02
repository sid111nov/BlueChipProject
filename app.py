import streamlit as st
import data.ticker_data as td
import pandas as pd
import warnings



st.title("McDonalds Stock Price Predictor")

st.write("**Note**: This is **not a financial advice**, *nor am I a fianncial advisor*, this is simply a **demo** app on timeseries forecasting")

col1, col2 = st.columns(2)

last_known_price = None
last_known_volume = None
dividends = 0
dow_jones = None
nasdaq_composits = None

df = td.getAggregateDataFrame()




with col1:
    last_known_price = st.number_input(label="Enter last known/closing Price")
    dividends = st.number_input(label="Enter Dividend")

with col2:
    last_known_volume = st.number_input(label="Enter last known/closing Volume")
    dow_jones = st.number_input(label="Enter Dow Jones Industrial Average")
    nasdaq_composits = st.number_input(label="Enter Nasdaq Composit")



if df.empty:
    st.error("Cached data is empty or invalid!")
else:
    st.dataframe(df)
    
if(st.button("Submit",type='primary')):
    st.title(last_known_price)