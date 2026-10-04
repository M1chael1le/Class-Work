from datetime import date, timedelta
import pandas as pd
import plotly.express as px
import streamlit as st
import yfinance as yf

END = date.today()
START = date.today() - timedelta(days=365)

st.set_page_config(layout="wide",
                   page_title="Stock Price Analysis")

st.title("Stock Analysis")

st.sidebar.title("Inputs")
ticker = st.sidebar.text_input("Enter stock ticker symbol",
                               value="AAPL")
col1, col2 = st.sidebar.columns(2)
start_date = col1.date_input("Start Date", START)
end_date = col2.date_input("End Date", END)
short_ma = st.sidebar.slider("Short Moving Average",
                           min_value= 5,
                           max_value= 50,
                           value= 20,
                           step = 1)
long_ma = st.sidebar.slider("Long Moving Average",
                           min_value= 50,
                           max_value= 200,
                           value= 100,
                           step = 1)

run_analysis = st.sidebar.button("Run Analysis",
                                 type= "primary")


def get_stock_data(ticker, start_date, end_date):
    try:
        data = yf.download(ticker, start_date, end_date)
        if data.empty:
            return None, f"No data for {ticker}"
        if isinstance(data.columns, pd.MultiIndex):
            data.columns = data.columns.get_level_values(0)
        return data, f" Successfully downloaded {ticker}"
    except Exception as e:
        return None, f"Download failed due to {e}"
if run_analysis:
    data, message = get_stock_data(ticker, start_date, end_date)
    if data is None:
        st.error(message)
    else:
        st.success(message)
        data["MA_short"] = data["Close"].rolling(short_ma).mean()
        data["MA_long"] = data["Close"].rolling(long_ma).mean()
        fig = px.line(data, y=["Close", "MA_short", "MA_long"],
                      title="Moving Average Comparison")
        st.plotly_chart(fig)