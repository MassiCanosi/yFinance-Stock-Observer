# Creates Candlesticks
from bokeh.io import output_notebook
from bokeh.layouts import layout
from bokeh.plotting import figure, show
from bokeh.models import ColumnDataSource
from math import pi

def candlesticks_chart(df):

       output_notebook()

       # Convert to ColumnDataSource
       source = ColumnDataSource(data=df)

       # Create a new plot with datetime x-axis
       p = figure(x_axis_type="datetime", width=1000, height=400, title="Candlestick Chart")

       # Define the width of the candlestick bars
       bar_width = 12 * 60 * 60 * 1000  # 12 hours in ms (to make bars wide enough on the plot)

       # Plot the wicks (high and low)
       p.segment(x0='Date', x1='Date', y0='Low', y1='High', color="black", source=source)

       # Plot the body (open and close)
       p.vbar(x='Date', width=bar_width, top='Open', bottom='Close', fill_color="green", line_color="red", 
              source=source, legend_label="Rising (Open < Close)")
       p.vbar(x='Date', width=bar_width, top='Close', bottom='Open', fill_color="red", line_color="blue", 
              source=source, legend_label="Falling (Open > Close)")

       # Rotate the x-axis labels for better readability
       p.xaxis.major_label_orientation = pi / 4

       # Customize legend
       p.legend.location = "top_left"
       p.legend.title = "Price Movement"

       return p