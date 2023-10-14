import reverse_geocode
import pycountry_convert as pc

from data.get_data import get_df

from time import time

# # Get DataFrame
df = get_df()


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
                country_code = result.get("country_code")
                try:
                    continent_code = pc.country_alpha2_to_continent_code(country_code)
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


start = time()
print(get_country_continent(df))
print(time() - start)
