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
    sum_chart = px.line(
        dfy, x="year", y="value", title="Number of meteorites landings by year"
    )
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
        df, x=["year"], title="Cumulative Number of meteorites landings by year"
    )
    return cumsum_chart


def draw_pie_chart(df: pd.DataFrame, number_of_values=None):
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


def draw_hist_country_continent(df: pd.DataFrame, column="continent"):  # country
    def get_continent_name(continent_code: str) -> str:
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
                    # if result.get("country") == "Chile":
                    #     print(result, coord)
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
