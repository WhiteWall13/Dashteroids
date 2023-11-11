from data.get_data import test_connection
from dashboard.graphs.charts import (
    draw_sum_chart,
    draw_cumsum_chart,
    draw_pie_chart,
    draw_bar_country_continent,
    draw_hist_distrib,
)
from dashboard.graphs.maps import draw_scatter_mapbox, draw_density_mapbox

import pandas as pd
import geopandas as gpd
import plotly.express as px
from dash import html
from dash import dcc
from dash import dash_table

intro_text = "This dataset presents a comprehensive collection of meteorite landings, meticulously compiled by The Meteoritical Society. It encapsulates the details of each meteorite landing, each entry enriched with information about the location, type, mass, and discovery details of the meteorites. The data, originally curated by Javier de la Torre, is a testament to the extensive history of meteoritic events that our planet has witnessed. The fields within this dataset range from geographical coordinates to mass in grams, and from the year of landing to the classification of meteorites. Notably, the dataset distinguishes between 'valid' meteorites—those that have been confirmed and cataloged—and 'relict' meteorites, which have undergone significant alteration due to Earth's weathering processes. The year 1969 marks a pivotal moment in history with the first human landing on the Moon, igniting the conquest of space. This event sparked a heightened interest in space and, consequently, meteorites began to be recorded with greater scrutiny. As a result, the default value for the year in our visualizations is set to 1969, reflecting the era when humanity turned its gaze starward, leading to an increased documentation of meteoritic discoveries. You can click on the button below to see the dataset."
datatable_text = "The data table provides a detailed and sortable view of the meteorite landings. It serves as a foundational tool for researchers and enthusiasts alike, offering a granular look at each individual event. This table is the gateway to deeper insights and is the basis for all subsequent visual analyses."
piechart_text = "The pie chart of meteorite classes reveals the distribution of various types of meteorites. The prominence of certain classes over others can be attributed to a combination of factors, including the frequency of these types in space, their survival rate through Earth's atmosphere, and the ease with which they can be found and identified on Earth's surface."
linechart_text = "Those histogram, line chart and cumulative sum charts depict the distribution of meteorite landings over the years, showing both the total count and the cumulative count. The scarcity of data in earlier years can be attributed to factors such as less systematic data recording, reduced efforts in meteorite searches, and the natural erosion and gradual disappearance of older meteorites, making their identification increasingly challenging as time passes."
bar_text = "The bar chart displaying the number of meteorites found per continent highlights intriguing geographical patterns. The high numbers in Antarctica and Africa could be influenced by the visibility and preservation conditions in desert and ice environments, which are conducive to meteorite recovery. The size of the continent, human population density, and the extent of scientific exploration also play significant roles in these figures."
map_text = "The scatter map and density visualization provide a spatial perspective of meteorite landings. The absence of meteorites in aquatic regions is not indicative of their actual fall patterns but rather reflects the difficulty in locating and retrieving meteorites from these environments."


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
    # Draw bar chart
    bar_country_continent = draw_bar_country_continent(df)
    # Draw histogram
    histogram_distrib = draw_hist_distrib(df)

    # Set variables
    year_min = int(df["year"].min())
    year_max = int(df["year"].max())
    fifty_min = (year_min // 50) * 50
    fifty_max = ((year_max + 49) // 50) * 50
    step = 50

    # Add reversed color
    colorscales = get_colorscales()

    # Get Layers
    layers = [
        "white-bg",
        "open-street-map",
        "carto-positron",
        "carto-darkmatter",
        "basic",
        "streets",
        "outdoors",
        "light",
        "dark",
        "satellite",
        "satellite-streets",
    ]

    # Get Connection
    connection = test_connection()

    return html.Div(
        [
            # Title
            html.H1("Dashteroids - Data Dashboard", style={"text-align": "center"}),
            dcc.Markdown(
                intro_text,
                style={"margin-top": "20px"},
            ),
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
            dcc.Markdown(
                datatable_text,
                style={"margin-top": "20px"},
            ),
            # Pie chart
            html.Div(
                [
                    html.H2("Pie Chart"),
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
                        value=10,
                        tooltip={"placement": "bottom", "always_visible": True},
                    ),
                    dcc.Markdown(id="pie_description", style={"margin-top": "20px"}),
                ]
            ),
            dcc.Markdown(
                piechart_text,
                style={"margin-top": "20px"},
            ),
            # Sum chart
            html.Div(
                [
                    html.H2("Histogram and Line Charts"),
                    dcc.Dropdown(
                        id="sum-type",
                        options=[
                            {"label": "Histogram", "value": "Histogram"},
                            {"label": "Sum", "value": "Sum"},
                            {"label": "Cumulative Sum", "value": "Cumsum"},
                        ],
                        value="Histogram",
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
                        value=[1969, year_max],
                        tooltip={"placement": "bottom", "always_visible": True},
                    ),
                    dcc.Markdown(id="sum-description", style={"margin-top": "20px"}),
                ]
            ),
            dcc.Markdown(
                linechart_text,
                style={"margin-top": "20px"},
            ),
            # Bar chart
            html.Div(
                [
                    html.H2("Bar chart"),
                    dcc.Graph(id="bar_country", figure=bar_country_continent),
                ]
            ),
            dcc.Markdown(
                bar_text,
                style={"margin-top": "20px"},
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
                    html.P(
                        "Select your layer :",
                        id="color-layer",
                    ),
                    dcc.Dropdown(
                        id="layer_dd",
                        options=layers,
                        value="basic",
                    ),
                    html.P(
                        "Select your color :",
                        id="color-label",
                        style={"display": "none"},
                    ),
                    dcc.Dropdown(
                        id="color_dd",
                        options=colorscales,
                        value="ylorrd_r",
                        style={"display": "none"},
                    ),
                    dcc.Graph(id="map", style={"width": "100%", "height": "600px"}),
                    dcc.RangeSlider(
                        id="year-slider-map",
                        min=year_min,
                        max=year_max,
                        step=1,
                        marks={
                            i: str(i) for i in range(fifty_min, fifty_max + 1, step)
                        },
                        value=[1969, year_max],
                        tooltip={"placement": "bottom", "always_visible": True},
                    ),
                    dcc.Markdown(id="map-description", style={"margin-top": "20px"}),
                ],
                style={"display": "none" if not connection else "block"},
            ),
            dcc.Markdown(
                map_text,
                style={"margin-top": "20px"},
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
        ],
        style={
            "max-width": "1200px",
            "margin": "0 auto",
            "padding": "0 20px",
            "text-align": "justify",
        },
    )
