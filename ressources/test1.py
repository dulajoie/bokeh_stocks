import configparser
from alpha_vantage.timeseries import TimeSeries
import pandas as pd
from bokeh.plotting import figure, show, curdoc
from bokeh.layouts import column
from math import pi



# read config file
config = configparser.ConfigParser()
config.read('ressources/config.ini')

## read alphavantage key 
alpha_key=config['alpha']['key']

stock_name = config['stock']['name']
index_name = config['index']['name']

ts = TimeSeries(key = alpha_key)

data_stock, meta_data = ts.get_daily(stock_name)

data_index, meta_index = ts.get_daily(index_name)

def dict_to_df(data_dict):
    df = pd.DataFrame.from_dict(data_dict, orient='index') 
    df = df.reset_index()
    df = df.rename(index=str, columns={"index": "date", "1. open": "open", "2. high": "high", "3. low": "low", "4. close": "close","5. volume":"volume"})
    #Changing to datetime
    df['date'] = pd.to_datetime(df['date'])
    #Changing open, close ... to float
    df['open'] = df['open'].astype('float')
    df['close'] = df['close'].astype('float')
    df['high'] = df['high'].astype('float')
    df['low'] = df['low'].astype('float')
    #Sort according to date
    df = df.sort_values(by=['date'])
    inc = df.close > df.open
    dec = df.open > df.close
    return df, inc, dec

df_stock, inc, dec = dict_to_df(data_stock)

# df_index, inc_index, dec_index = dict_to_df(data_index)

w = 12*60*60*1000 # half day in ms

TOOLS = "pan,wheel_zoom,box_zoom,reset,save"
title = stock_name  # + ' Chart corr with '+ index_name + ' = ' + str(df_stock.close.corr(df_index.close)) 

price = figure(x_axis_type="datetime", tools=TOOLS, plot_width=1000, title = title)
price.xaxis.major_label_orientation = pi/4
price.grid.grid_line_alpha=0.3 

# 
# ratio0 = df_index.close[0]
# price.segment(df_stock.date, df_stock.high*ratio0/df_index.close, df_stock.date, df_stock.low*ratio0/df_index.close, color="black")
# price.vbar(df_stock.date[inc], w, df_stock.open[inc]*ratio0/df_index.close[inc], df_stock.close[inc]*ratio0/df_index.close[inc], fill_color="#22FAFF", line_color="black")
# price.vbar(df_stock.date[dec], w, df_stock.open[dec]*ratio0/df_index.close[dec], df_stock.close[dec]*ratio0/df_index.close[dec], fill_color="#FAEEEE", line_color="black")


price.segment(df_stock.date, df_stock.high, df_stock.date, df_stock.low, color="black")
price.vbar(df_stock.date[inc], w, df_stock.open[inc], df_stock.close[inc], fill_color="#22FA22", line_color="black")
price.vbar(df_stock.date[dec], w, df_stock.open[dec], df_stock.close[dec], fill_color="#F2583E", line_color="black")

volumes = figure(x_axis_type="datetime", tools=TOOLS, plot_width=1000, plot_height=300, x_range=price.x_range)
volumes.vbar(df_stock.date[inc], w, 0, df_stock.volume[inc], fill_color="#22FA22", line_color="black")
volumes.vbar(df_stock.date[dec], w, 0, df_stock.volume[dec], fill_color="#F2583E", line_color="black")

curdoc().add_root(column(price,volumes))