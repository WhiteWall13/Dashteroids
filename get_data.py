import pandas as pd
from sodapy import Socrata

def fetch_data_from_api(number_of_values=1000000):
    """
    Fetches data from an API and returns it as a DataFrame.
    
    Args:
        number_of_values (int, optional): The number of values to retrieve from the API. Defaults to 1000000.
    
    Returns:
        pandas.DataFrame or None: The retrieved data as a DataFrame, or None if an error occurs.
    """
    try:
        # Create client and retrieve data from API
        client = Socrata("data.nasa.gov", None)
        results = client.get("gh4g-9sfh", limit=number_of_values)
        
        # Create DataFrame from API results
        df = pd.DataFrame.from_records(results)
        
        return df
    
    except Exception as e:
        print(f"Error fetching data from API: {e}")
        return None

def setup_df(df: pd.DataFrame):
    """
    A function that takes a pandas DataFrame as input and performs the following operations:
    - Drops the last two columns of the DataFrame
    - Extracts the year from the 'year' column by splitting the string on '-' and selecting the first element
    The modified DataFrame is then returned as the output.

    Parameters:
    - df (pd.DataFrame): The input DataFrame

    Returns:
    - pd.DataFrame: The modified DataFrame
    """
    # Drop the last two columns
    df = df.iloc[:, :-2]
    
    # Extract the year from the timestamp
    df['year'] = df['year'].str.split('-').str[0]
    
    return df

def get_data():
    """
    Fetches data from an API and sets it up in a dataframe.

    Returns:
        pandas.DataFrame: The dataframe containing the fetched and setup data.
    """
    df = fetch_data_from_api()
    df = setup_df(df)
    return df