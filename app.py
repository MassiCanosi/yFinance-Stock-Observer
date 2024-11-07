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
from utils.News_scraper import get_news

# !!! 
#   extract_stock_data(company, stock_name) 
#   return share_price_data, Open_Price_against_Date, dividends_df, Dividends, YoY_deltaViz, traded_volumes
# !!!



### TODO: FIXA GLI ERRORI SE INSERIMENTO TICKER SBAGLIATO (REF: SWAL FIRE)



###################/// APP CONFIG ///####################

app = Flask(__name__, static_folder='static', template_folder='templates')

app.config.from_object(Config)  # Load the configuration
KEY_TOKEN = app.config['SECRET_KEY']

Compress(app)

cache = Cache(app, config={'CACHE_TYPE': 'simple'})


###################/// APP ROUTES ///####################
@app.route('/')
def landingpage():
    return render_template('index.html', title="Home Page")

@app.route('/getStockData', methods=['POST', 'GET'])
def getStockData():
    try:

        stock_name = request.json.get('ticker')
        stock_name_upper = stock_name.upper()
        app.logger.info(f"/getstockData: {stock_name_upper}")

        share_price_data, Open_Price_against_Date, dividends_df, Dividends, YoY_deltaViz, traded_volumes = extract_stock_data(stock_name)

        if isinstance(Dividends, str):

            Open_Price_against_Date_data, Open_Price_against_Date_layout  = render_plotly_chart(Open_Price_against_Date)
            YoY_JSON_data, YoY_JSON_layout = render_plotly_chart(YoY_deltaViz)
            dividends_data = Dividends
            volumes_data, volumes_layout = render_plotly_chart(traded_volumes)

            return jsonify(success=True, message="Data processed successfully!",
                            Open_Price_against_Date_data = Open_Price_against_Date_data, Open_Price_against_Date_layout = Open_Price_against_Date_layout,
                            YoY_JSON_data= YoY_JSON_data, YoY_JSON_layout= YoY_JSON_layout,
                            dividends_data = dividends_data,
                            volumes_data = volumes_data, volumes_layout = volumes_layout
                        )

        else:

            Open_Price_against_Date_data, Open_Price_against_Date_layout  = render_plotly_chart(Open_Price_against_Date)
            YoY_JSON_data, YoY_JSON_layout = render_plotly_chart(YoY_deltaViz)
            dividends_data, dividends_layout = render_plotly_chart(Dividends)
            volumes_data, volumes_layout = render_plotly_chart(traded_volumes)

            return jsonify(success=True, message="Data processed successfully!",
                            Open_Price_against_Date_data = Open_Price_against_Date_data, Open_Price_against_Date_layout = Open_Price_against_Date_layout,
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

@app.route('/getStockNews', methods=['POST', 'GET'])
def getStockNews():
    stock_name = request.json.get('ticker')
    stock_name_upper = stock_name.upper()
    app.logger.info(f"/getStockNews: {stock_name_upper}")

    data = get_news(stock_name_upper)

    data_len = len(data)

    return jsonify(success=True, message="Data processed successfully!", data = data, data_len = data_len)


@app.route('/news')
def newspage():
    return render_template('news.html', title="News")


@app.route('/deepdive')
def deepdive():
    return render_template('deepdive.html')


@app.route('/risktables')
def risktables():
    return render_template('esgtables.html')


if __name__ == '__main__':
    app.debug = True
    app.run(port=8080, host="0.0.0.0")