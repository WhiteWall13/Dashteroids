import pandas as pd
import geopandas as gpd
from shapely.geometry import Point
import plotly.express as px


def draw_scatter_mapbox(gdf: gpd.GeoDataFrame, color="ylorrd_r", dark_mode=False):
    # gdf = gdf.dropna(subset=["mass"])
    map = px.scatter_mapbox(
        gdf,
        title="Scatter map of meteorites landings",
        lat=gdf.geometry.y,
        lon=gdf.geometry.x,
        hover_name="name",
        zoom=1,
        # TODO: Setup size
        # size="mass",
        # size_min=5,
        # size_max=15,
        color="year",
        color_continuous_scale=color,
    )
    if dark_mode:
        map.update_layout(mapbox_style="white-bg")
    return map


def draw_density_mapbox(gdf: gpd.GeoDataFrame):
    """
    Generates a density mapbox using a GeoDataFrame.

    Args:
        gdf (gpd.GeoDataFrame): The GeoDataFrame containing the data to be plotted.

    Returns:
        map: The density mapbox plot.

    """
    map = px.density_mapbox(
        gdf,
        title="Density map of meteorites landingss",
        lat="reclat",
        lon="reclong",
        z="id",
        radius=10,
        center=dict(lat=0, lon=180),
        zoom=1,
        # mapbox_style="stamen-terrain",
    )
    return map
