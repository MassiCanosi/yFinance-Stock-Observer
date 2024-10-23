from flask import Flask, render_template, request, jsonify, current_app, send_file, redirect, url_for, session
from flask_compress import Compress
from flask_caching import Cache
from flask_session import Session
import json
import plotly
import plotly.express as px
import os
from config import Config
from utils.render_plotly_chart import render_plotly_chart
from bokeh import embed

from utils.DataElaboration import extract_stock_data 
# !!! 
#   extract_stock_data(company, stock_name) 
#   return share_price_data, Open_Price_against_Date, dividends_df, Dividends, YoY_deltaViz, traded_volumes
# !!!


###################/// APP CONFIG ///####################

app = Flask(__name__, static_folder='static', template_folder='templates')


app.config.from_object(Config)  # Load the configuration
KEY_TOKEN = app.config['SECRET_KEY']


Compress(app)

cache = Cache(app, config={'CACHE_TYPE': 'simple'})

@app.route('/')
def landingpage():
    return render_template('index.html')

@app.route('/getStockData', methods=['POST', 'GET'])
def getStockData():
    try:

        stock_name = request.json.get('ticker')
        stock_name_upper = stock_name.upper()
        app.logger.info(f"/getstockData: {stock_name_upper}")

        share_price_data, Open_Price_against_Date, dividends_df, Dividends, YoY_deltaViz, traded_volumes = extract_stock_data(stock_name)

        Open_Price_against_Date_JSON = json.dumps(embed.json_item(Open_Price_against_Date, "openprice"))
        YoY_JSON_data, YoY_JSON_layout = render_plotly_chart(YoY_deltaViz)
        dividends_data, dividends_layout = render_plotly_chart(Dividends)
        volumes_data, volumes_layout = render_plotly_chart(traded_volumes)

        return jsonify(success=True, message="Data processed successfully!",
                        Open_Price_against_Date_JSON_data = Open_Price_against_Date_JSON,
                        YoY_JSON_data=YoY_JSON_data, YoY_JSON_layout=YoY_JSON_layout,
                        dividends_data = dividends_data, dividends_layout = dividends_layout,
                        volumes_data = volumes_data, volumes_layout = volumes_layout
                    )
    
    except Exception as e:
            app.logger.info(f"Errore: {e}")
            return jsonify(success=False, message=str(e))


@app.route('/explore')
def explorepage():

    return render_template('explore.html', title="Historic Data")



if __name__ == '__main__':
    app.debug = True
    app.run(port=8080, host="0.0.0.0")