import dash
from dash import dcc, html
from dash import dash_table
from dash.dependencies import Input, Output
import plotly.express as px
import configparser


from data.get_data import *
from dashboard.graphs.maps import *
from dashboard.graphs.charts import *


# Config parser
config = configparser.ConfigParser()
config.read("config.ini")

# Get DataFrame
df = get_df()

# Get GeoDataFrame
gdf = get_geodf(df)

# Get DataFrame without Geolocation
table_df = df.drop("geolocation", axis=1)

# print(df)

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
# Draw Pie Chart and get number of classes
class_pie_chart, number_of_classes = draw_pie_chart(df)

# Set variables
year_min = int(df["year"].min())
year_max = int(df["year"].max())
fifty_min = (year_min // 50) * 50
fifty_max = ((year_max + 49) // 50) * 50
step = 50

# Layout
app.layout = html.Div(
    [
        html.H1("Dashteroids"),
        dash_table.DataTable(
            # Table
            id="datatable",
            columns=[
                {"name": "Name", "id": "name"},
                {"name": "ID", "id": "id"},
                {"name": "Name Type", "id": "nametype"},
                {"name": "Rec Class", "id": "recclass"},
                {"name": "Mass (g)", "id": "mass"},
                {"name": "Fall", "id": "fall"},
                {"name": "Year", "id": "year"},
                {"name": "Latitude", "id": "reclat"},
                {"name": "Longitude", "id": "reclong"},
            ],
            data=table_df.to_dict("records"),
            sort_action="native",
            page_size=10,
            # style_table={"height": "400px", "overflowY": "auto"},
        ),
        # Pie chart
        dcc.Graph(id="class_pie_chart", figure=class_pie_chart),
        dcc.Slider(
            id="class-slider",
            min=1,
            max=number_of_classes,
            step=1,
            marks={i: str(i) for i in range(1, number_of_classes + 1) if i % 20 == 0},
            value=number_of_classes,
        ),
        dcc.Markdown(id="pie_description", style={"margin-top": "20px"}),
        # Sums charts
        dcc.Dropdown(
            id="sum-type",
            options=[
                {"label": "Sum", "value": "Sum"},
                {"label": "CumSum", "value": "Cumsum"},
            ],
            value="Sum",
        ),
        dcc.Graph(id="sum", style={"width": "100%", "height": "100%"}),
        dcc.RangeSlider(
            id="year-slider-sum",
            min=year_min,
            max=year_max,
            step=1,
            marks={i: str(i) for i in range(fifty_min, fifty_max + 1, step)},
            value=[fifty_min, year_max],
        ),
        dcc.Markdown(id="sum-description", style={"margin-top": "20px"}),
        # Maps
        dcc.Dropdown(
            id="map-type",
            options=[
                {"label": "Scatter", "value": "Scatter"},
                {"label": "Density", "value": "Density"},
            ],
            value="Scatter",
        ),
        dcc.Graph(id="map", style={"width": "100%", "height": "100%"}),
        dcc.RangeSlider(
            id="year-slider-map",
            min=year_min,
            max=year_max,
            step=1,
            marks={i: str(i) for i in range(fifty_min, fifty_max + 1, step)},
            value=[year_min, year_max],
        ),
        dcc.Markdown(id="map-description", style={"margin-top": "20px"}),
    ]
)


@app.callback(
    [Output("map-description", "children"), Output("map", "figure")],
    [Input("map-type", "value"), Input("year-slider-map", "value")],
)
def update_map_description_and_figure(map_type, year_range):
    year_min, year_max = year_range
    filtered_gdf = gdf[(gdf["year"] >= year_min) & (gdf["year"] <= year_max)]

    map_description = f"*{map_type} map of geolocation of asteroids between {year_min} and {year_max}.*"

    if map_type == "Scatter":
        map_figure = draw_scatter_mapbox(filtered_gdf)
    elif map_type == "Density":
        map_figure = draw_density_mapbox(filtered_gdf)
    else:
        map_figure = None

    return map_description, map_figure


@app.callback(
    [Output("sum-description", "children"), Output("sum", "figure")],
    [Input("sum-type", "value"), Input("year-slider-sum", "value")],
)
def update_sum_description_and_figure(sum_type, year_range):
    year_min, year_max = year_range
    filtered_df = df[(df["year"] >= year_min) & (df["year"] <= year_max)]

    sum_description = (
        f"*{sum_type} of meteorite landing by year between {year_min} and {year_max}.*"
    )

    if sum_type == "Sum":
        sum_figure = draw_sum_chart(filtered_df)
    elif sum_type == "Cumsum":
        sum_figure = draw_cumsum_chart(filtered_df)
    else:
        # Handle other sum types here if needed
        sum_figure = None

    return sum_description, sum_figure


@app.callback(
    [Output("class_pie_chart", "figure"), Output("pie_description", "children")],
    [Input("class-slider", "value")],
)
def update_pie_chart_and_description(selected_value):
    updated_pie_chart = draw_pie_chart(df, number_of_values=selected_value)
    pie_description = f"*Pie chart showing {selected_value} most represented classes.*"
    return updated_pie_chart[0], pie_description


def run_app(debug=False):
    app.run_server(debug=debug)
