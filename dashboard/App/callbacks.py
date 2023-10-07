from dashboard.graphs.maps import draw_scatter_mapbox, draw_density_mapbox
from dashboard.graphs.charts import draw_sum_chart, draw_cumsum_chart, draw_pie_chart

from dash.dependencies import Input, Output
import pandas as pd
import geopandas as gpd


def get_callbacks(app, df: pd.DataFrame, gdf: gpd.GeoDataFrame):
    """
    A function that defines multiple callbacks for updating various components in the app based on user interactions such as maps, sum charts, and pie chart.

    Parameters:
    - app: An instance of the Dash application.

    Returns:
    - A tuple of callback functions, each responsible for updating a specific set of components in the app.
    """

    # Map Callback
    @app.callback(
        [
            Output("map-description", "children"),
            Output("map", "figure"),
            Output("color_dd", "style"),
            Output("color-label", "style"),
        ],
        [
            Input("map-type", "value"),
            Input("year-slider-map", "value"),
            Input("color_dd", "value"),
            Input("layer_dd", "value"),
        ],
    )
    def update_map_description_and_figure(map_type, year_range, color, layer):
        """
        Updates the map description and figure based on the selected map type, year range, and color.

        Parameters:
            map_type (str): The type of map to display. Valid values are "Scatter" and "Density".
            year_range (tuple): The range of years to filter the data by. Format: (year_min, year_max).
            color (str): The color value to use for the map.

        Returns:
            map_description (str): The description of the map based on the selected map type and year range.
            map_figure (object): The figure object representing the map.
            color_dropdown_style (dict): The style object for the color dropdown.
        """
        year_min, year_max = year_range
        filtered_gdf = gdf[(gdf["year"] >= year_min) & (gdf["year"] <= year_max)]

        map_description = f"*{map_type} map of geolocation of meteorites landing between {year_min} and {year_max}.*"
        color_dropdown_style = {"display": "none"}
        # color_label

        if map_type == "Scatter":
            map_figure = draw_scatter_mapbox(filtered_gdf, color=color, layer=layer)
            color_dropdown_style = {}
        elif map_type == "Density":
            map_figure = draw_density_mapbox(filtered_gdf, layer=layer)
        else:
            map_figure = None

        return map_description, map_figure, color_dropdown_style, color_dropdown_style

    # Sum charts Callback
    @app.callback(
        [Output("sum-description", "children"), Output("sum", "figure")],
        [Input("sum-type", "value"), Input("year-slider-sum", "value")],
    )
    def update_sum_description_and_figure(sum_type, year_range):
        """
        Updates the sum description and figures based on the sum type and year range.

        Parameters:
            sum_type (str): The type of sum to calculate.
            year_range (tuple): The range of years to consider.

        Returns:
            tuple: A tuple containing the updated sum description and figure.
                - sum_description (str): The updated sum description.
                - sum_figure (object): The updated sum figure.
        """
        year_min, year_max = year_range
        filtered_df = df[(df["year"] >= year_min) & (df["year"] <= year_max)]

        sum_description = f"*{sum_type} of meteorites landing by year between {year_min} and {year_max}.*"

        if sum_type == "Sum":
            sum_figure = draw_sum_chart(filtered_df)
        elif sum_type == "Cumsum":
            sum_figure = draw_cumsum_chart(filtered_df)
        else:
            sum_figure = None

        return sum_description, sum_figure

    # Pie chart Callback
    @app.callback(
        [Output("class_pie_chart", "figure"), Output("pie_description", "children")],
        [Input("class-slider", "value")],
    )
    def update_pie_chart_and_description(selected_value):
        """
        Update the pie chart and its description based on the selected value.

        Args:
            selected_value (int): The number of values to be represented in the pie chart.

        Returns:
            tuple: A tuple containing the updated pie chart figure and the pie chart description.
                - figure (object): The updated pie chart figure.
                - description (str): The description of the pie chart.
        """
        updated_pie_chart = draw_pie_chart(df, number_of_values=selected_value)
        pie_description = (
            f"*Pie chart showing {selected_value} most represented classes.*"
        )
        return updated_pie_chart[0], pie_description
