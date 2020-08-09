from pandas_datareader import data
import pandas as pd

#Define List of Stock Tickers
tickers = ["TWTR","INO","GPS","TSLA","AZN","TLRY","JMIA","NVAX","CGC"]
#Define Function to Collect Data
def get_data(tickers):
    start_date = '2018-08-27'
    end_date = '2020-08-01'
    datum = dict()
    df_ = dict()
    
    for ticker in tickers:
        datum = data.DataReader(ticker,'yahoo',start_date,end_date)
        df_[ticker] = datum 
        df_[ticker].to_csv(f"~/Desktop/mystockdashboard/data/{ticker}.csv")

    return df_

#Call function
get_data(tickers)
