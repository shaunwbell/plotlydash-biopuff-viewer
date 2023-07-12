import os
import json
import redis
import pandas as pd

from dash import Dash, html
import dash_design_kit as ddk
import plotly.express as px

import db

import tasks
from theme import theme


app = Dash(__name__)
server = app.server  # expose server variable for Procfile

def serve_layout():    

    def map_figures(df):
        fig = px.scatter_geo(df, lat='latitude', lon='longitude',
                            hover_name="trajectory_id", projection='orthographic', color='trajectory_id'
                            )
        fig.update_geos(resolution=50,lataxis_showgrid=True, lonaxis_showgrid=True,
                        projection_rotation=dict(lon=200, lat=50, roll=0),
                        lataxis_range=[52,72.5], lonaxis_range=[180,240])
        fig.update_layout(height=300, margin={"r":0,"t":0,"l":0,"b":0})
        
        return fig

    def empty_figures():
        fig = px.scatter_geo(projection='orthographic')
        fig.update_geos(resolution=50,lataxis_showgrid=True, lonaxis_showgrid=True,
                        projection_rotation=dict(lon=200, lat=50, roll=0),
                        lataxis_range=[52,72.5], lonaxis_range=[180,240])
        fig.update_layout(height=300, margin={"r":0,"t":0,"l":0,"b":0})

        return fig

    try:
        new_df = get_data()
        locmap = map_figures(new_df)
    except:
        locmap = empty_figures()

    return ddk.App(
        [
            ddk.Header(
                [
                    ddk.Logo(src=app.get_asset_url("logo.png")),
                    ddk.Title("Periodic Updates on Time Series Data"),
                ]
            ),
            ddk.Card(                
                width=50,                
                children=[
                ddk.CardHeader(title="ADCP Location Analysis"),
                ddk.Graph(
                    id="graph-adcp",
                    figure=adcpfig,
            ),
            html.Br(),
                ],
                theme=theme,
            )
        ]
    )


# Set layout to a function so that it is called on-the-fly when the
# application is loaded in the web browser
app.layout = serve_layout

if __name__ == "__main__":
    app.run_server()
