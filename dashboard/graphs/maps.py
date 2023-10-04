import geopandas as gpd
from shapely.geometry import Point
import plotly.express as px


def draw_scatter_mapbox(gdf: gpd.GeoDataFrame, color="ylorrd_r", dark_mode=False):
    gdf = gdf.dropna(subset=["mass"])
    exponent = 0.3
    gdf["power_mass"] = gdf["mass"] ** exponent
    map = px.scatter_mapbox(
        gdf,
        title="Scatter map of meteorites landings depending on the mass",
        lat=gdf.geometry.y,
        lon=gdf.geometry.x,
        # hover_name="name",
        # hover_data=["name", "mass", "year"],
        center={"lat": 40, "lon": 0},
        zoom=1,
        size="power_mass",
        size_max=15,
        color="year",
        color_continuous_scale=color,
    )
    if dark_mode:
        map.update_layout(mapbox_style="white-bg")
    map.update_traces(
        hovertemplate="%{customdata[0]}<br>Mass (g): %{customdata[1]}<br>Year: %{customdata[2]}",
        customdata=gdf[["name", "mass", "year"]].values,
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
        title="Density map of meteorites landings",
        lat="reclat",
        lon="reclong",
        z="id",
        radius=10,
        center=dict(lat=0, lon=180),
        zoom=1,
        # mapbox_style="stamen-terrain",
    )
    return map
