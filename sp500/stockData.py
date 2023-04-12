import datetime as dt
import yfinance as yf
from dateutil.relativedelta import relativedelta




def getData(numYears):
    endDate =  (dt.datetime.now().strftime("%Y-%m-%d"))
    # minus a year
    startDate = dt.datetime.now() - relativedelta(years=numYears)
    startDate = startDate.strftime('%Y-%m-%d')
    spy_ohlc_df = yf.download('SPY', end =endDate, start =startDate,interval = "1d")

    return spy_ohlc_df