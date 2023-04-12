import requests
import pandas as pd
import time

from tqdm import tqdm

API_KEY = None

def chain_condenser(data, putCall):

    l_records = []

    put_Call_Exp_Date_Map = data["putExpDateMap"] if putCall == 'PUT' else data["callExpDateMap"]

    for expiration in put_Call_Exp_Date_Map.keys():
        for strike in put_Call_Exp_Date_Map[expiration]:

            keys = [
                "putCall","symbol","exchangeName","bid","ask","last","bidSize",
                "askSize", "lastSize","highPrice","lowPrice","openPrice","closePrice",
                "totalVolume","tradeTimeInLong","quoteTimeInLong",
                "volatility","delta","gamma","theta","vega","rho","openInterest",
                "strikePrice","expirationDate","daysToExpiration","expirationType",
                "percentChange","intrinsicValue","inTheMoney", "pennyPilot"
            ]

            record = put_Call_Exp_Date_Map[expiration][strike][0]
            record = { key: record[key] for key in keys }

            record["isDelayed"]       = data["isDelayed"]
            record["interestRate"]    = data["interestRate"]
            record["underlying"]      = data["symbol"]
            record["underlyingPrice"] = data["underlyingPrice"]

            percentInTheMoney = (record["strikePrice"] - data["underlyingPrice"]) / data["underlyingPrice"] * 100
            record["percentInTheMoney"] = percentInTheMoney if record["putCall"] == "PUT" else (-1 * percentInTheMoney)
            record["collateral"] = record['last'] * 100 #TODO : Check the multiple for collateral is 100 or lower?

            l_records.append(record)

            # TESTIT: view first iteration
            # print(record)
            # quit()

    return l_records

def get_option_chain(symbol, putCall):
    resp = requests.get(
        url = "https://api.tdameritrade.com/v1/marketdata/chains",
        params = {
            "apikey": API_KEY,
            "symbol": symbol
        },
    )
    return chain_condenser(resp.json(), putCall)

def snapshot(other_assets_symbols, putCall):
    symbols = list(pd.read_html('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies', header = 0)[0]['Symbol'])

    chains = []
    for symbol in tqdm([*symbols, *other_assets_symbols]):
        try:
            chain = get_option_chain(symbol, putCall)
            chains += (chain)
            time.sleep(1)

        except Exception as e:
            print(e)
            None

    return pd.DataFrame(chains)
