# Creates Candlesticks
import plotly.graph_objects as go
import pandas as pd
import finplot as fplt

def candlesticks_chart(df, company_name):
        
    fig = go.Figure(data=[go.Candlestick(
        x=df['Date'],
            open=df['Open'],
            high=df['High'],
            low=df['Low'],
            close=df['Close']),
            ])
    
    fig.update_layout(title=f"{company_name} Candlesticks")
    fig.update_layout(height=500)
    fig.update_layout(hovermode = 'x')

    return fig