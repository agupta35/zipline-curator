import pandas as pd
import sp500 as data
import os

data.options.API_KEY = 'SIJAKDDBCB4BDMA8MPBJ4C6HV7E6IECQ' #TODO: Ask user to set key in environment variable

other_assets = pd.read_csv("files/List of Top 100 ETFs.csv") #pd.read_csv("files/etfs_US_list_1739.csv") #For more exhaustuive list
other_assets_symbols = other_assets['Symbol'].tolist()

# Check if pickle exists, else build data
stocks = pd.read_pickle("stockData.pkl") \
            if os.path.exists("stockData.pkl") \
                else data.stockData.getData(1)

#%% Cache data for future runs
stocks.to_pickle("stockData.pkl")

stocks.to_csv('files/spy.csv', header=True, index=False)

start_session = pd.Timestamp('2016-1-1', tz='utc')
end_session = pd.Timestamp('2018-1-1', tz='utc')






