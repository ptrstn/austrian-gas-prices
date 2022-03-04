from pandas import DataFrame
from plotly import express

import pandas


vienna_sup = pandas.read_csv("data/vienna_SUP.csv")
stations = pandas.read_csv("data/gas_stations.csv")

data = pandas.merge(vienna_sup, stations)

df = data[["timestamp", "price", "postal_code"]].copy()

addresses = data[["timestamp", "price", "postal_code", "name", "address"]]

min_prices_per_postal: DataFrame = (
    df.groupby(["timestamp", "postal_code"])["price"].min().reset_index()
)
mins = min_prices_per_postal.merge(addresses)

fig = express.line(
    mins,
    x="timestamp",
    y="price",
    color="postal_code",
    title="Minimum Super 95 prices per district",
    # hover_data=["name", "address"]
)
fig.update_traces(mode="markers+lines", hovertemplate=None)
fig.update_layout(hovermode="x")  # x unified

fig.show()
