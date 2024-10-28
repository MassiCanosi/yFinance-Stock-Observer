#Source
import yfinance as yf

#Elaboration
import pandas as pd
import numpy as np
import json

from datetime import datetime

# Handle Warnings
import warnings
warnings.filterwarnings("ignore", category=FutureWarning) 

# Data Viz
import plotly.express as px
from bokeh.plotting import figure, show
from bokeh.models import ColumnDataSource
from math import pi
from bokeh.io import output_notebook
from bokeh.layouts import layout
from utils.Creates_Candlesticks import candlesticks_chart

def extract_stock_data(stock_name): 

    ''' 
    Extract insights relative to a specific stock.

    :param filename: JSON file to load
    :param company: Company to be analyzed
    :param stockname: ticker symbol
    
    :return: graphs and stats related to the specific stock
    '''

    ticker = yf.Ticker(stock_name)
    company_name = ticker.info['longName']

    # Convert the dictionary to a pandas DataFrame
    share_price_data = ticker.history(period="max")
    share_price_data = share_price_data.reset_index()
    share_price_data['Date'] = pd.to_datetime(share_price_data['Date'])

    Open_Price_against_Date = candlesticks_chart(share_price_data)

    dividends_df = pd.DataFrame(ticker.dividends).reset_index()

    if dividends_df.empty:
        Dividends = f"{company_name} does not currently pay a cash dividend at this time."
    else:
        Dividends = px.line(dividends_df, x='Date', y='Dividends', title=f'{company_name} Dividends')

    share_price_data['Date'] = pd.to_datetime(share_price_data['Date'])
    share_price_data['Year'] = share_price_data['Date'].apply(lambda x: x.year)

    YoY_DeltaVolume = share_price_data.pivot_table(index='Year', values='Volume', aggfunc='sum').reset_index()

    YoY_DeltaVolume['Delta YoY'] = YoY_DeltaVolume['Volume'].diff().fillna(np.nan)
    YoY_DeltaVolume['Delta % YoY'] = round((YoY_DeltaVolume['Volume'].diff()/YoY_DeltaVolume['Volume'].shift())*100,2).fillna(np.nan)[2:]

    YoY_DeltaVolume['Trend'] = YoY_DeltaVolume['Delta YoY'].apply(lambda x: 'Up' if x>0 else ('Down' if x<0 else np.nan))

    YoY_deltaViz = px.bar(YoY_DeltaVolume, x='Year', y='Delta % YoY', barmode='relative', color='Trend', text_auto=True, title= f'{company_name} YoY Volume Trend')

    traded_volumes = px.line(share_price_data, x='Date', y='Volume', title= f'{company_name} YoY Volume Trend')

    return share_price_data, Open_Price_against_Date, dividends_df, Dividends, YoY_deltaViz, traded_volumes