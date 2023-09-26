import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import configparser

from get_data import *
from maps import *
from charts import *

# Config parser
config = configparser.ConfigParser()
config.read("config.ini")

# Get DataFrame
df = get_df()

# Get GeoDataFrame
gdf = get_geodf(df)

# Create Dash App
app = dash.Dash(__name__)

# Set MapBox Token
px.set_mapbox_access_token(config["TOKEN"]["mapbox_token"])

# Draw Maps
# Draw Scatter Mapbox
scatter_mapbox = draw_scatter_mapbox(gdf)
# Draw Density Mapbox
density_mapbox = draw_density_mapbox(gdf)

# Draw Charts
# Draw Sum Chart
sum_chart = draw_sum_chart(df)
# Draw CumSum Chart
cumsum_chart = draw_cumsum_chart(df)

# Set variables
year_min = int(df["year"].min())
year_max = int(df["year"].max())
decade_min = (year_min // 10) * 10
decade_max = ((year_max + 9) // 10) * 10
step = 50

# Layout
app.layout = html.Div(
    [
        html.H1("Dashteroids"),
        dcc.Dropdown(
            id="map-type",
            options=[
                {"label": "Scatter", "value": "scatter"},
                {"label": "Density", "value": "density"},
            ],
            value="scatter",
        ),
        dcc.Graph(id="map", style={"width": "100%", "height": "100%"}),
        # TODO: Fix map slider
        dcc.RangeSlider(
            id="year-slider",
            min=year_min,
            max=year_max,
            step=1,
            marks={i: str(i) for i in range(decade_min, decade_max + 1, step)},
            value=[year_min, year_max],
        ),
        dcc.Dropdown(
            id="chart-type",
            options=[
                {"label": "Sum", "value": "sum"},
                {"label": "CumSum", "value": "cumsum"},
            ],
            value="sum",
        ),
        dcc.Graph(id="sum-chart-type", style={"width": "100%", "height": "100%"}),
        # TODO: Fix slider end (2010 max year and should be 2020)
        dcc.RangeSlider(
            id="year-slider",
            min=year_min,
            max=year_max,
            step=1,
            marks={i: str(i) for i in range(decade_min, decade_max + 1, step)},
            value=[year_min, year_max],
        ),
    ]
)


@app.callback(
    Output("map", "figure"), [Input("map-type", "value"), Input("year-slider", "value")]
)
def update_map(selected_map_type, year_range):
    year_min, year_max = year_range
    filtered_gdf = gdf[(gdf["year"] >= year_min) & (gdf["year"] <= year_max)]

    if selected_map_type == "scatter":
        return draw_scatter_mapbox(filtered_gdf)
    elif selected_map_type == "density":
        return draw_density_mapbox(filtered_gdf)


@app.callback(
    Output("sum-chart-type", "figure"),
    [Input("chart-type", "value"), Input("year-slider", "value")],
)
def update_sum(selected_sum_type, year_range):
    year_min, year_max = year_range
    filtered_df = df[(df["year"] >= year_min) & (df["year"] <= year_max)]

    if selected_sum_type == "sum":
        return draw_sum_chart(filtered_df)
    elif selected_sum_type == "cumsum":
        return draw_cumsum_chart(filtered_df)


# Execute App
if __name__ == "__main__":
    app.run_server(debug=True)
