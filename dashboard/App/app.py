import pandas as pd
import dash
import plotly.express as px
import configparser

from data.get_data import get_geodf
from dashboard.app.layout import app_layout
from dashboard.app.callbacks import get_callbacks


def run_app(df: pd.DataFrame, debug: bool = False) -> None:
    """
    Run the Dash app.

    Args:
        df (pd.DataFrame): The DataFrame to be used in the app.
        debug (bool, optional): Whether to run the app in debug mode. Defaults to False.
    """
    # Get GeoDataFrame
    gdf = get_geodf(df)

    # Config parser
    config = configparser.ConfigParser()
    config.read("config.ini")

    # Set MapBox Token
    px.set_mapbox_access_token(config["TOKEN"]["mapbox_token"])

    # Create Dash App
    app = dash.Dash(__name__)

    # Get Layout
    app.layout = app_layout(df, gdf)

    # Get Callbacks
    get_callbacks(app, df, gdf)

    # Run App
    app.run_server(debug=debug)
