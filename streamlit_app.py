import random
from datetime import datetime, timedelta

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
import yfinance as yf

# Page config
st.set_page_config(page_title="Financial Sentiment Analyzer", layout="wide")

# Sidebar
st.sidebar.title("Controls")
ticker = st.sidebar.text_input("Enter Stock Ticker", value="AAPL")
days = st.sidebar.slider("Days of Historical Data", 1, 30, 7)

# Main content
st.title("Financial Sentiment Analysis Dashboard")


# Function to get stock data
@st.cache_data
def get_stock_data(ticker, days):
    try:
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        df = yf.download(ticker, start=start_date, end=end_date)
        df.reset_index(inplace=True)  # Reset index to make Date a column
        return df
    except Exception as e:
        st.error(f"Error fetching stock data: {str(e)}")
        # Return empty DataFrame with expected columns
        return pd.DataFrame(columns=["Date", "Close", "Volume"])


# Function to analyze text sentiment (replace with your actual model)
def analyze_sentiment(text):
    # This is where you'd call your LLM API
    # For demo, returning random sentiment between -1 and 1
    return random.uniform(-1, 1)


# Get stock data
df = get_stock_data(ticker, days)

if not df.empty:
    # Create columns for layout
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Stock Price Movement")
        fig = px.line(df, x="Date", y="Close", title=f"{ticker} Stock Price")
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader("Volume Analysis")
        fig = px.bar(df, x="Date", y="Volume", title=f"{ticker} Trading Volume")
        st.plotly_chart(fig, use_container_width=True)
else:
    st.warning("No stock data available for the selected ticker.")

# Text analysis section
st.subheader("Real-time Sentiment Analysis")
user_text = st.text_area("Enter financial news or analysis text:", height=100)

if st.button("Analyze Sentiment"):
    if user_text.strip():  # Only analyze if there's text
        with st.spinner("Analyzing..."):
            sentiment = analyze_sentiment(user_text)

            # Create gauge chart for sentiment
            fig = go.Figure(
                go.Indicator(
                    mode="gauge+number",
                    value=sentiment,
                    domain={"x": [0, 1], "y": [0, 1]},
                    title={"text": "Sentiment Score"},
                    gauge={
                        "axis": {"range": [-1, 1]},
                        "bar": {"color": "darkblue"},
                        "steps": [
                            {"range": [-1, -0.5], "color": "red"},
                            {"range": [-0.5, 0.5], "color": "gray"},
                            {"range": [0.5, 1], "color": "green"},
                        ],
                    },
                )
            )
            st.plotly_chart(fig, use_container_width=True)

            # Display sentiment interpretation
            if sentiment > 0.5:
                st.success("This text has a strong positive sentiment!")
            elif sentiment > 0:
                st.info("This text has a slightly positive sentiment.")
            elif sentiment > -0.5:
                st.warning("This text has a slightly negative sentiment.")
            else:
                st.error("This text has a strong negative sentiment!")
    else:
        st.warning("Please enter some text to analyze.")

# Historical sentiment analysis
st.subheader("Recent News Sentiment History")

# Create historical sentiment data
dates = pd.date_range(end=datetime.now(), periods=10, freq="D")
sentiments = [random.uniform(-1, 1) for _ in range(10)]
headlines = [f"Sample news headline {i+1}" for i in range(10)]

# Create DataFrame with proper structure
news_df = pd.DataFrame({"Date": dates, "Sentiment": sentiments, "News": headlines})

# Plot historical sentiment
fig = px.line(news_df, x="Date", y="Sentiment", title="Historical Sentiment Analysis")
st.plotly_chart(fig, use_container_width=True)

# Display recent news with sentiment
st.subheader("Recent News Analysis")
for _, row in news_df.iterrows():
    sentiment_color = "green" if row["Sentiment"] > 0 else "red"
    st.markdown(
        f"""
    <div style='padding: 10px; border-radius: 5px; margin: 5px 0; 
                background-color: {"rgba(0,255,0,0.1)" if row["Sentiment"] > 0 else "rgba(255,0,0,0.1)"}'>
        <p style='margin: 0;'><b>{row['Date'].strftime('%Y-%m-%d')}</b></p>
        <p style='margin: 0;'>{row['News']}</p>
        <p style='margin: 0; color: {sentiment_color};'>Sentiment: {row['Sentiment']:.2f}</p>
    </div>
    """,
        unsafe_allow_html=True,
    )
