import pandas as pd
import plotly.express as px


#TODO slider or year selecter to choose first and last year

def draw_sum_chart(df: pd.DataFrame):
    """
    Generate a line chart of the number of asteroids per year based on the given DataFrame.

    Parameters:
    - df (pd.DataFrame): The DataFrame containing the data.

    Returns:
    - sum_chart: The line chart showing the number of asteroids per year.
    """
    # print(type(df['year'][0]))
    dfy = df.groupby('year').size().reset_index(name='value')
    # dfy = dfy[dfy["value"] > 1]
    sum_chart = px.line(dfy, x='year', y='value', title='Number of Asteroids by year')
    return sum_chart


def draw_cumsum_chart(df: pd.DataFrame):
    """
    Generate a cumulative sum chart using the given DataFrame.

    Parameters:
        df (pd.DataFrame): The DataFrame containing the data.

    Returns:
        cumsum_chart: The cumulative sum chart.
    """
    cumsum_chart = px.ecdf(df, x=["year"])
    return cumsum_chart