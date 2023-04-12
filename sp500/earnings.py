import pandas as pd
import asyncio 
import aiohttp
from tqdm import tqdm

import datetime as dt
import json
import logging
import requests
import time
import numpy as np

BASE_URL = 'https://finance.yahoo.com/calendar/earnings'
BASE_STOCK_URL = 'https://finance.yahoo.com/quote'
RATE_LIMIT = 2000.0
SLEEP_BETWEEN_REQUESTS_S = 60 * 60 / RATE_LIMIT
OFFSET_STEP = 100
TQDM_OFF = True

def get(symbol):
        """Gets the next earnings date of symbol
        Args:
            symbol: A ticker symbol
        Returns:
            Unix timestamp of the next earnings date
        Raises:
            Exception: When symbol is invalid or earnings date is not available
        """
        url = '{0}/{1}'.format(BASE_STOCK_URL, symbol)
        # print(url)
        try:
            page = requests.get(url)
            page_content = page.content.decode(encoding='utf-8', errors='strict')
            page_data_string = [row for row in page_content.split(
                '\n') if row.startswith('root.App.main = ')][0][:-1]
            page_data_string = page_data_string.split('root.App.main = ', 1)[1]
            page_data_dict = json.loads(page_data_string)
            page_data_json = json.loads(page_data_string)
            earn_date = page_data_json['context']['dispatcher']['stores']['QuoteSummaryStore']['calendarEvents']['earnings']['earningsDate'][0]['raw']
            return {'ticker': symbol, 'date' : dt.datetime.fromtimestamp(earn_date)}
        except:
            return {'ticker': symbol, 'date': np.nan}

def snapshot(other_assets_symbols, symbols=[]):
    if not symbols:
        symbols = list(pd.read_html('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies', header = 0)[0]['Symbol'])
    try:
        earnings_frame = []
        for ticker in tqdm([*symbols, *other_assets_symbols]):
            earnings_frame.append(get(ticker))
        earnings_frame = pd.DataFrame(earnings_frame)
        earnings_frame = earnings_frame.set_index('ticker')
        earnings_frame.index.name = 'stock'
        
        return (earnings_frame)
    except:
        raise Exception('\n\n!!!!!!!!!!!! Rate limit Was hit !!!!!!!!!!!!!\n\n')