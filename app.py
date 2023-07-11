import os
import json
import redis
import pandas as pd

from dash import Dash, html
import dash_design_kit as ddk

import db

import tasks
from theme import theme

app = Dash(__name__)
server = app.server  # expose server variable for Procfile

df = db.get_counts()
print(df)
# def serve_layout():
#     new_df = get_dataframe()

#     return ddk.App(
#         [
#             ddk.Header(
#                 [
#                     ddk.Logo(src=app.get_asset_url("logo.png")),
#                     ddk.Title("Periodic Updates on Time Series Data"),
#                 ]
#             ),
#             ddk.Card(
#                 children=[
#                     ddk.CardHeader(title="Timeseries Analysis"),
#                     ddk.Graph(
#                         id="graph",
#                         figure={
#                             "data": [
#                                 {
#                                     "x": new_df["time"],
#                                     "y": new_df["value"],
#                                     "type": "bar",
#                                 }
#                             ],
#                             "layout": {"title": "Index"},
#                         },
#                     ),
#                 ]
#             ),
#             html.Br(),
#             ddk.Card(
#                 children=[
#                     ddk.Title("Updated Dataframe Point"),
#                     ddk.DataTable(
#                         id="table",
#                         columns=[{"name": i, "id": i} for i in new_df.columns],
#                         data=new_df.tail().to_dict("records"),
#                         page_size=10,
#                         style_cell_conditional=[{"textAlign": "center"}],
#                     ),
#                 ]
#             ),
#         ],
#         theme=theme,
#     )


# Set layout to a function so that it is called on-the-fly when the
# application is loaded in the web browser
app.layout = serve_layout

if __name__ == "__main__":
    app.run_server()
