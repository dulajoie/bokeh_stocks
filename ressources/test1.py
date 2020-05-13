import configparser
from alpha_vantage.timeseries import TimeSeries
import pandas as pd
from bokeh.plotting import figure, show, curdoc
from math import pi



stock_name = "CATG.PAR"
# read config file
config = configparser.ConfigParser()
config.read('ressources/config.ini')

## read alphavantage key 
alpha_key=config['alpha']['key']

ts = TimeSeries(key = alpha_key)

data, meta_data = ts.get_daily(stock_name)

df = pd.DataFrame.from_dict(data, orient='index') 
df = df.reset_index()

df = df.rename(index=str, columns={"index": "date", "1. open": "open", "2. high": "high", "3. low": "low", "4. close": "close","5. volume":"volume"})

#Changing to datetime
df['date'] = pd.to_datetime(df['date'])

#Sort according to date
df = df.sort_values(by=['date'])


inc = df.close > df.open
dec = df.open > df.close


w = 12*60*60*1000 # half day in ms

TOOLS = "pan,wheel_zoom,box_zoom,reset,save"
title = stock_name + ' Chart'
p = figure(x_axis_type="datetime", tools=TOOLS, plot_width=1000, title = title)
p.xaxis.major_label_orientation = pi/4
p.grid.grid_line_alpha=0.3 
p.segment(df.date, df.high, df.date, df.low, color="black")
p.vbar(df.date[inc], w, df.open[inc], df.close[inc], fill_color="#22FA22", line_color="black")
p.vbar(df.date[dec], w, df.open[dec], df.close[dec], fill_color="#F2583E", line_color="black")
curdoc().add_root(p)