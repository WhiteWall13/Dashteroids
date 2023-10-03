import pandas as pd
import plotly.express as px


# TODO slider or year selecter to choose first and last year


def draw_sum_chart(df: pd.DataFrame):
    """
    Generate a line chart of the number of asteroids per year based on the given DataFrame.

    Parameters:
    - df (pd.DataFrame): The DataFrame containing the data.

    Returns:
    - sum_chart: The line chart showing the number of asteroids per year.
    """
    dfy = df.groupby("year").size().reset_index(name="value")
    sum_chart = px.line(dfy, x="year", y="value", title="Number of Asteroids by year")
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
        df, x=["year"], title="Cumulative Number of Asteroids by year"
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
        title="Class Distribution of Asteroids",
    )
    class_pie_chart.update_traces(textposition="inside", textinfo="percent+label")
    return class_pie_chart, len(recclass_counts)
