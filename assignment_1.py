import pandas as pd
import plotly.express as px
import streamlit as st
from datetime import date, timedelta
from stock import Stock

END = date.today()
START = date.today() - timedelta(days=365)

@st.cache_data
def load_stock(ticker, start, end, ma_window):
    stock = Stock(ticker, start, end, ma_window)
    return stock

st.set_page_config(layout="wide", page_title="Stock Analysis")
st.title("Stock Analysis")

tab1, tab2 = st.tabs(["Single Stock Analysis", "Portfolio Comparison"])

st.sidebar.title("Inputs")
ticker = st.sidebar.text_input("Enter stock ticker symbol",
                               value="AAPL")
col1, col2 = st.sidebar.columns(2)
start_date = col1.date_input("Start Date", START)
end_date = col2.date_input("End Date", END)
ma_window = st.sidebar.slider("Moving Average",
                              min_value= 5,
                              max_value= 200,
                              value= 50,
                              step = 1)

portfolio_tickers = st.sidebar.text_input("Enter stock ticker symbols",
                                         value="AAPL, MSFT, GOOG")

run_analysis = st.sidebar.button("Run Analysis",
                                 type= "primary")
if run_analysis:
    st.session_state["ran"] = True

with tab1:
    if st.session_state.get("ran"):
        with st.spinner("Loading data..."):
            stock = load_stock(ticker, start_date, end_date, ma_window)
        if stock.data is None:
            st.error(stock.message)
        else:
            st.success(stock.message)
            st.metric("Last Close", f"${stock.data['Close'].iloc[-1]:.2f}")
            st.metric("Trading Days", len(stock.data))
            st.metric("Cumulative Return", f"{stock.data['return'].sum():.2%}")
            fig = px.line(stock.data, y=["Close", "MA"], title=f"{stock.symbol} Close Price and {ma_window}-Day Moving Average")
            st.plotly_chart(fig)
            fig = stock.plot_performance()
            st.plotly_chart(fig)
            st.dataframe(stock.data['return'].describe())
            fig = stock.plot_return_dist()
            st.plotly_chart(fig)

with tab2:
    if st.session_state.get("ran"):
        tickers = [t.strip() for t in portfolio_tickers.split(",")]
        performance = {}
        for t in tickers:
            with st.spinner("Loading data..."):
                stock = load_stock(t, start_date, end_date, ma_window)
            if stock.data is None:
                st.error(stock.message)
            else:
                perf = stock.data['return'].cumsum()
                performance[stock.symbol] = perf - perf.iloc[0]
        if performance:
            df = pd.DataFrame(performance)
            fig = px.line(df, title="Cumulative Performance Comparison")
            st.plotly_chart(fig)







