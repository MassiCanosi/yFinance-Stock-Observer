import yfinance as yf

def get_news(stock_name):
    ticker = yf.Ticker('msft')

    news = ticker.news

    for info in news:
        title = info['title']
        type = info['type']
        publisher = info['publisher']
        if 'thumbnail' in info:
            thumbnail = info['thumbnail']['resolutions'][1]
        relatedTickers = info['relatedTickers']

    return title, type, publisher, thumbnail, relatedTickers