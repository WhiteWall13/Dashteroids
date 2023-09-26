import pandas as pd
import geopandas as gpd
from shapely.geometry import Point
import plotly.express as px


def clear_years(gdf: gpd.GeoDataFrame):
    """
    Clear years from a GeoDataFrame.

    Parameters:
        gdf (gpd.GeoDataFrame): The GeoDataFrame to clear the years from.

    Returns:
        gdf (gpd.GeoDataFrame): The GeoDataFrame with the years cleared.
    """
    gdf["year"] = gdf["year"].astype(float)
    gdf.loc[gdf["year"] < 1500, "year"] = pd.NA
    # TODO: Get current year instead of 2023
    gdf.loc[gdf["year"] > 2023, "year"] = pd.NA
    return gdf


def draw_scatter_mapbox(gdf: gpd.GeoDataFrame, color="ylorrd_r", year_min=1500):
    gdf.loc[gdf["year"] < year_min, "year"] = pd.NA
    # TODO: Change the scale
    map = px.scatter_mapbox(
        gdf,
        lat=gdf.geometry.y,
        lon=gdf.geometry.x,
        hover_name="name",
        zoom=1,
        # TODO: Setup size
        # size="mass",
        # size_max=15,
        color="year",
        color_continuous_scale=color,
    )
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
        lat="reclat",
        lon="reclong",
        z="id",
        radius=10,
        center=dict(lat=0, lon=180),
        zoom=1,
        mapbox_style="stamen-terrain",
    )
    return map
