import yfinance as yf

def get_news(stock_name):

    ticker = yf.Ticker(stock_name)

    news = ticker.news
    reduced_dict = dict()

    for i, info in enumerate(news):
        uuid = info['uuid']
        title = info['title']
        link = info['link']
        type = info['type']
        publisher = info['publisher']
        if 'thumbnail' in info:
            thumbnail = info['thumbnail']['resolutions'][0]['url']

        relatedTickers = info['relatedTickers']

        reduced_dict[i] = {"title": title, "link": link, "type": type, "publisher": publisher, "thumbnail": thumbnail, "relatedTickers": relatedTickers}

    return reduced_dict