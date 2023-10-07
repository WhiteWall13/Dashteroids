import pandas as pd
import geopandas as gpd
import plotly.express as px
import dash_html_components as html
import dash_core_components as dcc
from dash import dash_table


from data.get_data import *
from dashboard.graphs.charts import draw_sum_chart, draw_cumsum_chart, draw_pie_chart
from dashboard.graphs.maps import draw_scatter_mapbox, draw_density_mapbox


def get_colorscales():
    """
    Returns a list of named colorscales and their reversed versions.

    Returns:
        List[str]: The list of named colorscales and their reversed versions.
    """
    named_colorscales = px.colors.named_colorscales()
    reversed_colorscales = [color + "_r" for color in named_colorscales]
    return named_colorscales + reversed_colorscales


def app_layout(df: pd.DataFrame, gdf: gpd.GeoDataFrame):
    """
    Generate the layout of the Dash application.

    Parameters:
    - df (pd.DataFrame): The input DataFrame containing the data.
    - gdf (gpd.GeoDataFrame): The input GeoDataFrame containing the geolocation data.

    Returns:
    - html.Div: The layout of the Dash application.
    """
    # Get DataFrame without Geolocation
    table_df = df.drop("geolocation", axis=1)

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

    # Add reversed color
    colorscales = get_colorscales()

    connection = test_connection()

    return html.Div(
        [
            # Title
            html.H1("Dashteroids - Data Dashboard"),
            # Button
            html.Div(
                [
                    html.A(
                        "Dataset",
                        href="https://data.nasa.gov/Space-Science/Meteorite-Landings/gh4g-9sfh",
                        target="_blank",
                        style={
                            "display": "block",
                            "text-align": "center",
                            "margin": "20px auto",
                            "font-size": "18px",
                            "text-decoration": "none",
                            "color": "white",
                            "background-color": "blue",
                            "padding": "10px 20px",
                            "border-radius": "5px",
                            "width": "150px",
                        },
                    ),
                ],
                style={
                    "text-align": "center",
                    "display": "none" if not connection else "block",
                },
            ),
            # DataTable
            html.Div(
                [
                    html.H2("Data Table"),
                    dash_table.DataTable(
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
                    ),
                ]
            ),
            # Pie chart
            html.Div(
                [
                    html.H2("Class distribution"),
                    dcc.Graph(id="class_pie_chart", figure=class_pie_chart),
                    dcc.Slider(
                        id="class-slider",
                        min=1,
                        max=number_of_classes,
                        step=1,
                        marks={
                            i: str(i)
                            for i in range(1, number_of_classes + 1)
                            if i % 20 == 0
                        },
                        value=number_of_classes,
                        tooltip={"placement": "bottom", "always_visible": True},
                    ),
                    dcc.Markdown(id="pie_description", style={"margin-top": "20px"}),
                ]
            ),
            # Sum chart
            html.Div(
                [
                    html.H2("Sum charts"),
                    dcc.Dropdown(
                        id="sum-type",
                        options=[
                            {"label": "Sum", "value": "Sum"},
                            {"label": "Cumulative Sum", "value": "Cumsum"},
                        ],
                        value="Sum",
                    ),
                    dcc.Graph(id="sum", style={"width": "100%", "height": "100%"}),
                    dcc.RangeSlider(
                        id="year-slider-sum",
                        min=year_min,
                        max=year_max,
                        step=1,
                        marks={
                            i: str(i) for i in range(fifty_min, fifty_max + 1, step)
                        },
                        value=[fifty_min, year_max],
                        tooltip={"placement": "bottom", "always_visible": True},
                    ),
                    dcc.Markdown(id="sum-description", style={"margin-top": "20px"}),
                ]
            ),
            # Maps
            html.Div(
                [
                    html.H2("Maps"),
                    dcc.Dropdown(
                        id="map-type",
                        options=[
                            {"label": "Scatter Map", "value": "Scatter"},
                            {"label": "Density Map", "value": "Density"},
                        ],
                        value="Scatter",
                    ),
                    html.P("Select your color :"),  # TODO : Hide if density selected
                    dcc.Dropdown(
                        id="color_dd",
                        options=colorscales,
                        value="ylorrd_r",
                        style={"display": "none"},
                    ),
                    dcc.Graph(id="map", style={"width": "100%", "height": "800px"}),
                    dcc.RangeSlider(
                        id="year-slider-map",
                        min=year_min,
                        max=year_max,
                        step=1,
                        marks={
                            i: str(i) for i in range(fifty_min, fifty_max + 1, step)
                        },
                        value=[year_min, year_max],
                        tooltip={"placement": "bottom", "always_visible": True},
                    ),
                    dcc.Markdown(id="map-description", style={"margin-top": "20px"}),
                ],
                style={"display": "none" if not connection else "block"},
            ),
            # Conditionnal mesage
            html.Div(
                "You are currently running this Dashboard with no connection. All features can't be displayed.",
                id="connection-message",
                style={
                    "text-align": "center",
                    "font-size": "18px",
                    "color": "red",
                    "margin-top": "20px",
                    "display": "none" if connection else "block",
                },
            ),
        ]
    )


# Layout
# app.layout = html.Div(
#     [
#         html.H1("Dashteroids - Data Dashboard"),
#         # Button
#         html.Div(
#             [
#                 html.A(
#                     "Dataset",
#                     href="https://data.nasa.gov/Space-Science/Meteorite-Landings/gh4g-9sfh",
#                     target="_blank",
#                     style={
#                         "display": "block",
#                         "text-align": "center",
#                         "margin": "20px auto",
#                         "font-size": "18px",
#                         "text-decoration": "none",
#                         "color": "white",
#                         "background-color": "blue",
#                         "padding": "10px 20px",
#                         "border-radius": "5px",
#                         "width": "150px",
#                     },
#                 ),
#             ],
#             style={
#                 "text-align": "center",
#                 "display": "none" if not connection else "block",
#             },
#         ),
#         # DataTable
#         html.Div(
#             [
#                 html.H2("Data Table"),
#                 dash_table.DataTable(
#                     id="datatable",
#                     columns=[
#                         {"name": "Name", "id": "name"},
#                         {"name": "ID", "id": "id"},
#                         {"name": "Name Type", "id": "nametype"},
#                         {"name": "Rec Class", "id": "recclass"},
#                         {"name": "Mass (g)", "id": "mass"},
#                         {"name": "Fall", "id": "fall"},
#                         {"name": "Year", "id": "year"},
#                         {"name": "Latitude", "id": "reclat"},
#                         {"name": "Longitude", "id": "reclong"},
#                     ],
#                     data=table_df.to_dict("records"),
#                     sort_action="native",
#                     page_size=10,
#                 ),
#             ]
#         ),
#         # Pie chart
#         html.Div(
#             [
#                 html.H2("Class distribution"),
#                 dcc.Graph(id="class_pie_chart", figure=class_pie_chart),
#                 dcc.Slider(
#                     id="class-slider",
#                     min=1,
#                     max=number_of_classes,
#                     step=1,
#                     marks={
#                         i: str(i)
#                         for i in range(1, number_of_classes + 1)
#                         if i % 20 == 0
#                     },
#                     value=number_of_classes,
#                     tooltip={"placement": "bottom", "always_visible": True},
#                 ),
#                 dcc.Markdown(id="pie_description", style={"margin-top": "20px"}),
#             ]
#         ),
#         # Sum chart
#         html.Div(
#             [
#                 html.H2("Sum charts"),
#                 dcc.Dropdown(
#                     id="sum-type",
#                     options=[
#                         {"label": "Sum", "value": "Sum"},
#                         {"label": "Cumulative Sum", "value": "Cumsum"},
#                     ],
#                     value="Sum",
#                 ),
#                 dcc.Graph(id="sum", style={"width": "100%", "height": "100%"}),
#                 dcc.RangeSlider(
#                     id="year-slider-sum",
#                     min=year_min,
#                     max=year_max,
#                     step=1,
#                     marks={i: str(i) for i in range(fifty_min, fifty_max + 1, step)},
#                     value=[fifty_min, year_max],
#                     tooltip={"placement": "bottom", "always_visible": True},
#                 ),
#                 dcc.Markdown(id="sum-description", style={"margin-top": "20px"}),
#             ]
#         ),
#         # Maps
#         html.Div(
#             [
#                 html.H2("Maps"),
#                 dcc.Dropdown(
#                     id="map-type",
#                     options=[
#                         {"label": "Scatter Map", "value": "Scatter"},
#                         {"label": "Density Map", "value": "Density"},
#                     ],
#                     value="Scatter",
#                 ),
#                 html.P("Select your color :"),  # TODO : Hide if density selected
#                 dcc.Dropdown(
#                     id="color_dd",
#                     options=colorscales,
#                     value="ylorrd_r",
#                     style={"display": "none"},
#                 ),
#                 dcc.Graph(id="map", style={"width": "100%", "height": "800px"}),
#                 dcc.RangeSlider(
#                     id="year-slider-map",
#                     min=year_min,
#                     max=year_max,
#                     step=1,
#                     marks={i: str(i) for i in range(fifty_min, fifty_max + 1, step)},
#                     value=[year_min, year_max],
#                     tooltip={"placement": "bottom", "always_visible": True},
#                 ),
#                 dcc.Markdown(id="map-description", style={"margin-top": "20px"}),
#             ],
#             style={"display": "none" if not connection else "block"},
#         ),
#         # Conditionnal mesage
#         html.Div(
#             "You are currently running this Dashboard with no connection. All features can't be displayed.",
#             id="connection-message",
#             style={
#                 "text-align": "center",
#                 "font-size": "18px",
#                 "color": "red",
#                 "margin-top": "20px",
#                 "display": "none" if connection else "block",
#             },
#         ),
#     ]
# )
