import pandas as pd
import plotly.express as px
import reverse_geocode
import pycountry_convert as pc


def draw_sum_chart(df: pd.DataFrame):
    """
    Generate a line chart of the number of asteroids per year based on the given DataFrame.

    Parameters:
    - df (pd.DataFrame): The DataFrame containing the data.

    Returns:
    - sum_chart: The line chart showing the number of asteroids per year.
    """
    dfy = df.groupby("year").size().reset_index(name="value")
    sum_chart = px.line(dfy, x="year", y="value", title="Number of meteorites by year")
    return sum_chart


def draw_cumsum_chart(df: pd.DataFrame):
    """
    Generate a cumulative sum chart using the given DataFrame.

    Parameters:
        df (pd.DataFrame): The DataFrame containing the data.

    Returns:
        cumsum_chart: The cumulative sum chart.
    """
    cumsum_chart = px.ecdf(
        df, x=["year"], title="Cumulative Number of meteorites by year"
    )
    return cumsum_chart


def draw_pie_chart(df: pd.DataFrame, number_of_values=None):
    """
    Generate a pie chart to visualize the class distribution of meteorites.

    Parameters:
        df (pd.DataFrame): The DataFrame containing the meteorite data.
        number_of_values (int, optional): The number of values to include in the pie chart.
            If not provided, all values will be included.

    Returns:
        class_pie_chart (plotly.graph_objects.Figure): The generated pie chart.
        count (int): The number of unique recclass values included in the pie chart.
    """
    if number_of_values is None:
        recclass_counts = df["recclass"].value_counts()
    else:
        recclass_counts = df["recclass"].value_counts()[:number_of_values]
    class_pie_chart = px.pie(
        recclass_counts,
        values=recclass_counts.values,
        names=recclass_counts.index,
        title="Class Distribution of meteorites",
    )
    class_pie_chart.update_traces(textposition="inside", textinfo="percent+label")
    return class_pie_chart, len(recclass_counts)


def draw_bar_country_continent(df: pd.DataFrame, column="continent"):  # country
    def get_continent_name(continent_code: str) -> str:
        """
        Generate a bar plot showing the distribution of countries across continents.

        Parameters:
            df (pd.DataFrame): The DataFrame containing the data.
            column (str, optional): The name of the column in the DataFrame that contains the continent information. Defaults to "continent".

        Returns:
            None
        """
        continent_dict = {
            "NA": "North America",
            "SA": "South America",
            "AS": "Asia",
            "AF": "Africa",
            "OC": "Oceania",
            "EU": "Europe",
            "AQ": "Antarctica",
        }
        return continent_dict[continent_code]

    def get_country_continent(df):
        """
        Takes a DataFrame as input and performs reverse geocoding on the coordinates in the "reclat" and "reclong" columns.
        The function combines the latitude and longitude values to create a list of coordinates.
        It then iterates over each coordinate and performs reverse geocoding to obtain the country and continent values.
        If the reverse geocoding fails or the coordinates are (0.0, 0.0), the function appends None to the country and continent lists.
        Otherwise, it appends the country name to the country list and determines the continent name based on the country code.
        The country and continent values are added as new columns "country" and "continent" to the input DataFrame, which is then returned.

        Parameters:
        - df: A DataFrame containing the "reclat" and "reclong" columns.

        Returns:
        - df: The input DataFrame with additional columns "country" and "continent" containing the reverse geocoded values.
        """
        # Combine 'reclat' and 'reclong' columns to create a list of coordinates
        coords = list(zip(df["reclat"], df["reclong"]))

        # Initialize an empty list to store the country values
        country_values = []
        continent_values = []

        # Perform reverse geocoding with error handling
        for coord in coords:
            try:
                result = reverse_geocode.search([coord])[0]
                if result is None or coord == (0.0, 0.0):
                    country_values.append(None)
                    continent_values.append(None)
                else:
                    country_values.append(result.get("country"))
                    country_code = result.get("country_code")
                    try:
                        if country_code != "AQ":
                            continent_code = pc.country_alpha2_to_continent_code(
                                country_code
                            )
                        else:
                            continent_code = "AQ"
                        continent_name = get_continent_name(continent_code)
                        continent_values.append(continent_name)
                    except:
                        continent_values.append(None)
            except:
                # print(f"Error for coordinates {coord}: {e}")
                country_values.append(None)
                continent_values.append(None)

        # Add the "country" column to the DataFrame
        df["country"] = country_values
        df["continent"] = continent_values

        return df

    df = get_country_continent(df)
    fig = px.histogram(df, x=column, title=f"Number of meteorites by {column}")
    return fig


def draw_hist_distrib(df):
    """
    Generate a histogram to visualize the distribution of the number of meteorites per year.

    Parameters:
        df (DataFrame): The input DataFrame containing the meteorite data.

    Returns:
        None
    """
    # Create a new DataFrame with the number of meteorites per year
    meteorites_per_year = df["year"].value_counts().reset_index()
    meteorites_per_year.columns = ["year", "number_of_meteorites"]

    # Sort the DataFrame by year
    meteorites_per_year = meteorites_per_year.sort_values("year")

    # Create a histogram using Plotly Express
    fig = px.bar(
        meteorites_per_year,
        x="year",
        y="number_of_meteorites",
        labels={"year": "Year", "number_of_meteorites": "Number of Meteorites"},
        title="Distribution of the number of meteorites per year",
    )

    fig.update_layout(
        xaxis_type="category"
    )  # To treat 'year' as a categorical variable

    return fig
