# Creates Candlesticks
import plotly.graph_objects as go
import pandas as pd

def candlesticks_chart(df):
        
    fig = go.Figure(data=[go.Candlestick(
        x=df['Date'],
            open=df['Open'],
            high=df['High'],
            low=df['Low'],
            close=df['Close'])],
            )
    
    fig.update_layout(title="Candlesticks")
    fig.update_layout(height=500)

    return fig