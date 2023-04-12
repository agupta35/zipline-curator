import sp500 as data
import pandas as pd
import os
from zipline.data.bundles import register
from zipline.data.bundles.csvdir import csvdir_equities

data.options.API_KEY = 'SIJAKDDBCB4BDMA8MPBJ4C6HV7E6IECQ' #TODO: Ask user to set key in environment variable

other_assets = pd.read_csv("files/List of Top 100 ETFs.csv") #pd.read_csv("files/etfs_US_list_1739.csv") #For more exhaustuive list
other_assets_symbols = other_assets['Symbol'].tolist()

# Check if pickle exists, else build data
stocks = pd.read_pickle("stockData.pkl") \
            if os.path.exists("stockData.pkl") \
                else data.stockData.getData(1)

#%% Cache data for future runs
stocks.to_pickle("stockData.pkl")
stocks = stocks.reset_index()
stocks.reset_index(inplace=True)
stocks['Date'] = stocks['Date'].dt.strftime('%m-%d-%Y')
stocks = stocks.drop('index', axis=1)
stocks = stocks.rename(columns={'Adj Close':'close', 'High':'high','Date':'date', 'Open':'open', 'Close':'close','Volume':'volume','Low':'low'})
stocks['dividend'] = 0
stocks['split'] = 0
stocks.to_csv('data/daily/spy.csv', header=True, index=False)


start_session = pd.Timestamp('2022-6-1', tz='utc')
end_session = pd.Timestamp('2023-1-1', tz='utc')
register(
    'spy-prices-2010-2021',
    csvdir_equities(
        ['daily'],
        'data',
    ),
    calendar_name='NYSE', # US equities
    start_session=start_session,
    end_session=end_session
)




