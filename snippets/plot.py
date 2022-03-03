from plotly import express
from plotly import graph_objects
import pandas


df = pandas.read_csv("data/vienna_SUP.csv")

mins = df.groupby(["timestamp"]).min().reset_index()

fig = express.scatter(mins, x="timestamp", y="price")

fig = express.line(
    mins,
    x="timestamp",
    y="price",
)
# fig = graph_objects.Figure([graph_objects.Scatter(x=df['timestamp'], y=df['price'])])
fig.show()
