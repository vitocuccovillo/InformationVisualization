from bokeh.io import show, output_file
from bokeh.plotting import figure
from googlefinance.client import get_price_data, get_prices_data, get_prices_time_data

# Dow Jones
param = {
    'q': "AAPL", # Stock symbol (ex: "AAPL")
    'i': "60", # Interval size in seconds ("86400" = 1 day intervals)
    'x': "INDEXDJX", # Stock exchange symbol on which stock is traded (ex: "NASD")
    'p': "1M" # Period (Ex: "1Y" = 1 year)
}
# get price data (return pandas dataframe)
df = get_price_data(param)
print(df)

output_file("bars.html")

days = df.High.index.values
daysList = []

daysToPrint = 10

for d in days:
    if daysToPrint > 0:
        daysList.append(str(d)[:16])
        daysToPrint-=1
fruits = daysList

p = figure(x_range=fruits, plot_height=500, title="Valori azioni", plot_width=1000)
p.vbar(x=fruits, top=df.High.values, width=0.9)

p.xgrid.grid_line_color = None
p.y_range.start = 0

show(p)