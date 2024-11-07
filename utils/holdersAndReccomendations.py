import yfinance as yf 
import pandas as pd

def investors_and_reccomendations(stock_name):

    ''' 
    Extract insights relative to a specific stock.

    :param stockname: ticker symbol
    
    :return: stats related to the specific stock (risk, holders, reccomendations)
    '''

    ticker = yf.Ticker(stock_name)
    company_name = ticker.info['longName']

    major_holders_df = ticker.major_holders

    institutional_holders_df = ticker.institutional_holders
    institutional_holders_df['Shares'] = institutional_holders_df['Shares'].apply(lambda x: "{:,.0f}".format(x))
    institutional_holders_df['Value'] = institutional_holders_df['Value'].astype(float)
    institutional_holders_df['Value'] = institutional_holders_df['Value'].apply(lambda x: "{:,.0f}".format(x))

    recommendations_df = ticker.recommendations


    major_risks = pd.DataFrame(ticker.sustainability).reset_index().rename(columns={'index': 'Risk'})
    major_risks = major_risks.loc[21:].reset_index(drop=True)

    mapping = {
        'adult': 'Adult',
        'alcoholic': 'Alcoholic',
        'animalTesting': 'Animal Testing',
        'controversialWeapons': 'Controversial Weapons',
        'furLeather': 'Fur Leather',
        'gambling': 'Gambling',
        'gmo': 'GMO',
        'militaryContract': 'Military Contract',
        'nuclear': 'Nuclear',
        'pesticides': 'Pesticides',
        'palmOil': 'Palm Oil',
        'coal': 'Coal',
        'tobacco': 'Tobacco'
    }

    major_risks['Labels'] = major_risks['Risk'].map(mapping)

    major_risks = major_risks.dropna()
    major_risks = major_risks.drop('Risk', axis=1)
    major_risks.insert(0, 'Labels', major_risks.pop('Labels'))
    major_risks = major_risks.reset_index(drop=True)

    return major_holders_df, institutional_holders_df, recommendations_df, major_risks