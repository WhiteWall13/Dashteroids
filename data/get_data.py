import pandas as pd
from sodapy import Socrata
import geopandas as gpd
from shapely.geometry import Point
import datetime
import requests


def fetch_data_from_api(number_of_values=1000000):
    """
    Fetches data from an API and returns it as a pandas DataFrame.

    Parameters:
        number_of_values (int): The number of values to retrieve from the API.
            Default is 1000000.

    Returns:
        pandas.DataFrame: A DataFrame containing the retrieved data.
    """
    # Create client and retrieve data from API
    client = Socrata("data.nasa.gov", None)
    results = client.get("gh4g-9sfh", limit=number_of_values)

    # Create DataFrame from API results
    df = pd.DataFrame.from_records(results)

    return df


def fetch_data_from_csv(file_path="data/files/Meteorite_Landings.csv"):
    """
    Fetches data from a CSV file and performs some data transformations.

    Parameters:
    file_path (str): The path to the CSV file. Defaults to "files/Meteorite_Landings.csv".

    Returns:
    pandas.DataFrame: The DataFrame containing the fetched and transformed data.
    """
    # Read the CSV file into a DataFrame
    df = pd.read_csv(file_path)

    # Rename the 'GeoLocation' column to 'geolocation' and strip the quotes
    df.rename(columns={"GeoLocation": "geolocation"}, inplace=True)
    df["geolocation"] = df["geolocation"].str.strip('"')

    # Rename the 'mass (g)' column to 'mass'
    df.rename(columns={"mass (g)": "mass"}, inplace=True)

    # Format the 'geolocation' column as dictionaries
    df["geolocation"] = df.apply(
        lambda row: {"latitude": str(row["reclat"]), "longitude": str(row["reclong"])},
        axis=1,
    )

    return df


def get_data():
    """
    Get data from either an API or a CSV file.

    Returns:
    - df (pandas.DataFrame): The data fetched from the API or CSV file.
    """
    try:
        df = fetch_data_from_api()
    except:
        df = fetch_data_from_csv()
    return df


def clear_df(df):
    """
    Clears the given DataFrame by dropping the last two columns, extracting the year from the timestamp,
    converting the id to int, mass to float, year to numeric, reclat to numeric, and reclong to numeric.
    It also drops rows where the year is greater than the current year.

    Parameters:
    - df (pandas.DataFrame): The DataFrame to be cleared.

    Returns:
    - pandas.DataFrame: The cleared DataFrame.
    """
    # Drop the last two columns
    df = df.iloc[:, :-2]

    # Extract the year from the timestamp
    try:
        df["year"] = df["year"].str.split("-").str[0]
    except:
        pass

    # Convert the id to int
    df["id"] = df["id"].astype(int)
    # Convert the mass to float
    df["mass"] = df["mass"].astype(float)
    # Convert the year to float
    df["year"] = df["year"].astype(float)
    # Convert the reclat to float
    df["reclat"] = df["reclat"].astype(float)
    # Convert the reclong to float
    df["reclong"] = df["reclong"].astype(float)

    # Drop rows where the year is greater than the current year
    df.loc[df["year"] > datetime.datetime.now().year, "year"] = pd.NA

    return df


def get_df():
    """
    Get the dataframe by retrieving the data using the `get_data()` function.
    Then clear the dataframe using the `clear_df()` function.

    Returns:
        DataFrame: The cleaned dataframe.
    """
    # Get the data
    df = get_data()

    # Clear the data
    df = clear_df(df)

    return df


def get_geodf(df: pd.DataFrame):
    """
    Generate a GeoDataFrame from a DataFrame by dropping rows with missing geolocation and creating Points based on the longitude and latitude values.

    Parameters:
    - df (pd.DataFrame): The input DataFrame containing the geolocation information.

    Returns:
    - gdf (gpd.GeoDataFrame): The generated GeoDataFrame with the added geometry column.
    """
    # Drop rows with missing geolocation
    df = df.dropna(subset=["geolocation"])

    # Create Points
    geometry = [
        Point(float(point["longitude"]), float(point["latitude"]))
        for point in df["geolocation"]
    ]

    # Create a GeoDataFrame
    gdf = gpd.GeoDataFrame(df, geometry=geometry)
    return gdf


def test_connection(url: str = "http://www.google.com") -> bool:
    """
    Check if a connection can be established to the given URL.

    Args:
        url: The URL to test the connection to. Defaults to "http://www.google.com".

    Returns:
        True if a connection can be established, False otherwise.
    """
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return True
    except:
        pass
    return False
