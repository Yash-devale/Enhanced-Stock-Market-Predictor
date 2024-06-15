import streamlit as st
import pandas as pd
import datetime
import requests
from bs4 import BeautifulSoup
import yfinance as yf
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt

# Function to fetch historical data from Yahoo Finance
def fetch_historical_data(ticker, start_date, end_date):
    stock = yf.Ticker(ticker)
    df = stock.history(start=start_date, end=end_date)
    df.reset_index(inplace=True)
    return df

# Function to scrape stock data from Yahoo Finance
def scrape_stock_data():
    urls = {
         'Nifty 50': 'https://finance.yahoo.com/quote/%5ENSEI?p=%5ENSEI',
        'Sensex': 'https://finance.yahoo.com/quote/%5EBSESN?p=%5EBSESN',
        'NASDAQ': 'https://finance.yahoo.com/quote/%5EIXIC?p=%5EIXIC',
        'Dow Jones': 'https://finance.yahoo.com/quote/%5EDJI?p=%5EDJI',
        'S&P 500': 'https://finance.yahoo.com/quote/%5EGSPC?p=%5EGSPC',
        "Bitcoin USD": "https://finance.yahoo.com/quote/BTC-USD/",
        "Ethereum USD": "https://finance.yahoo.com/quote/ETH-USD/",
        "Gold": "https://finance.yahoo.com/quote/GC%3DF/",
        "Oil": "https://finance.yahoo.com/quote/CL%3DF/",
        "EUR/USD": "https://finance.yahoo.com/quote/EURUSD=X/"
    }
    
    data = {'Date': [datetime.date.today().strftime('%Y-%m-%d')]}
    for index, url in urls.items():
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        price_span = soup.find('div', {'class':'D(ib) Mend(20px)'})
        if price_span:
            price = price_span.find('span')
            if price:
                price_value = price.text.replace(',', '')
                data[index] = [float(price_value)]
            else:
                data[index] = [None]
        else:
            data[index] = [None]
    
    df = pd.DataFrame(data)
    return df

# Mock function to predict stock movement (simple linear regression model)
def predict_stock_movement(historical_data):
    historical_data['Date'] = pd.to_datetime(historical_data['Date'])
    historical_data['DayOfYear'] = historical_data['Date'].dt.dayofyear
    X = historical_data[['DayOfYear']]
    y = historical_data['Close']
    
    model = LinearRegression()
    model.fit(X, y)
    
    today_day_of_year = datetime.date.today().timetuple().tm_yday
    prediction = model.predict([[today_day_of_year]])
    return 'Up' if prediction[0] > historical_data['Close'].iloc[-1] else 'Down'

# Function to render the login page
def login():
    st.header("Predicting The Future Of Finance")
    st.text("Note:")
    st.text("This app is designed to help you make informed decisions, but it cannot guarantee profits.")
   
    st.sidebar.header("Login")
    
    username = st.sidebar.text_input("Username")
    password = st.sidebar.text_input("Password", type="password")
    if st.sidebar.button("Login"):
        st.session_state['logged_in'] = True
        st.session_state['username'] = username  # Initialize username in session_state

    # Developer contact information
    developer_expander = st.sidebar.expander('Contact Developer', expanded=False)
    with developer_expander:
        st.text('Developed By:')
        st.text("Yash Devale")
        st.text("Email_Id:")
        st.text('yashdevale1@outlook.com')
    # Contact form expander
    contact_expander = st.sidebar.expander('Contact Form', expanded=False)
    with contact_expander:
        name = st.text_input('Name')
        email = st.text_input('Email')
        message = st.text_area('Message', height=150)
        if st.button('Send Message'):
            # Here you can add code to handle the message submission, like sending an email or storing in a database
            st.success('Message sent successfully!')


# Function to render the logout button
def logout():
    if st.sidebar.button("Logout"):
        st.session_state['logged_in'] = False


# Main function
def main():
    st.set_page_config(page_title="Enhanced Stock Market Prediction", layout="wide", initial_sidebar_state="expanded")
    
    # Custom HTML header
    st.markdown(
        """
        <style>
            .header {
                background-color: #4CAF50;
                color: white;
                padding: 20px;
                text-align: center;
                font-size: 24px;
                font-family: Arial, sans-serif;
                margin-bottom: 30px;
            }
        </style>
        """
    , unsafe_allow_html=True)

    st.markdown('<p class="header">Welcome to Enhanced Stock Market Prediction</p>', unsafe_allow_html=True)
    
    if 'logged_in' not in st.session_state:
        st.session_state['logged_in'] = False
    
    if not st.session_state['logged_in']:
        login()
        return
    
    # Theme selection
    st.sidebar.subheader("Theme Settings")
    theme = st.sidebar.radio("Select Theme", ('Light', 'Dark'))
    if theme == 'Dark':
        dark_mode = """
        <style>
            body {
                color: white;
                background-color: #333333;
            }
            .header {
                background-color: #555555;
            }
        </style>
        """
        st.markdown(dark_mode, unsafe_allow_html=True)
    
    st.sidebar.write("Logged in as:", st.session_state.get('username', 'Guest'))  # Display username if logged in
    logout()

    # Sidebar for user inputs
    st.sidebar.header("User Input Parameters")
    
    
    selected_date = st.sidebar.date_input("Select a date", datetime.date.today())
    
    st.sidebar.write("Date Selected:", selected_date)
    
    # Ticker selection
    st.sidebar.subheader("Select Tickers")
    tickers = st.sidebar.multiselect("Select Tickers",['Nifty 50', 'Sensex', 'NASDAQ', 'Dow Jones', 'S&P 500', 
                      'Bitcoin USD', 'Ethereum USD', 'Gold', 'Oil', 'EUR/USD'])
    

    if not tickers:
        st.warning("Please select at least one ticker.")
        return
    # Display historical data and predictions
    for index in tickers:
        ticker = None
        if index == 'Nifty 50':
            ticker = '%5ENSEI'
        elif index == 'Sensex':
            ticker = '%5EBSESN'
        elif index == 'NASDAQ':
            ticker = '%5EIXIC'
        elif index == 'Dow Jones':
            ticker = '%5EDJI'
        elif index == 'S&P 500':
            ticker = '%5EGSPC'
        elif index == 'Nifty 50':
            ticker='%5ENSEI'
        elif index == 'Sensex':
             ticker='%5EBSESN'
        elif index ==  'NASDAQ': 
             ticker='%5EIXIC'
        elif index == 'Dow Jones':
            ticker='%5EDJI'
        elif index == 'S&P 500':
             ticker='%5EGSPC'
        elif index == 'Bitcoin USD':
          ticker='BTC-USD'
        elif index == 'Ethereum USD':
             ticker='ETH-USD'
        elif index == 'Gold':
             ticker = 'GC=F'
        elif index == 'Oil':
             ticker = 'CL=F'
        elif index == 'EUR/USD':
             ticker='EURUSD=X'
        
        if ticker:
            st.title(f"{index} Historical Data for {selected_date}")
            historical_data = fetch_historical_data(ticker, start_date="2023-01-01", end_date=selected_date.strftime("%Y-%m-%d"))
            st.write(historical_data)
            
            fig, ax = plt.subplots()
            ax.plot(historical_data['Date'], historical_data['Close'], label=f'{index} Close Price')
            ax.set_title(f'{index} Closing Prices')
            ax.set_xlabel('Date')
            ax.set_ylabel('Closing Price')
            ax.tick_params(axis='x', rotation=60)  # Rotate x-axis labels by 60 degrees
            ax.legend()
            st.pyplot(fig)
            
            if not historical_data.empty:
                prediction = predict_stock_movement(historical_data)
                if prediction == 'Up':
                    st.markdown(f"Prediction for {index} on {selected_date}: **The market is expected to go {prediction}**.")
                else:
                    st.markdown(f"Prediction for {index} on {selected_date}: **The market is expected to go {prediction}**.", unsafe_allow_html=True)

if 1==1:
    main()
