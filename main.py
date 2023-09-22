# import pandas as pd
# import json
# import requests

# url = "https://data.nasa.gov/resource/gh4g-9sfh.json"

# req = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})

# json_data = req.text

# data_dict = json.loads(json_data)
# print(data_dict)

# df = pd.DataFrame(data_dict)
# df = df.iloc[:, :-2]

# print(df.head())

import pandas as pd
from sodapy import Socrata
from datetime import datetime

# Unauthenticated client only works with public data sets. Note 'None'
# in place of application token, and no username or password:
client = Socrata("data.nasa.gov", None)

# Example authenticated client (needed for non-public datasets):
# client = Socrata("data.nasa.gov",
#                  "Dashteroids",
#                  username="nhmu13@gmail.com",
#                  password="")

# First 2000 results, returned as JSON from API / converted to Python list of
# dictionaries by sodapy.
max_int = 1000000
results = client.get("gh4g-9sfh", limit=max_int)

# Convert to pandas DataFrame
results_df = pd.DataFrame.from_records(results)

df = results_df.iloc[:, :-2]
# print(set(df['year']))
# print(set(df['nametype']))

# date_format = '%Y-%m-%dT%H:%M:%S.%f'

# # Convertissez la colonne 'year' en objets datetime en utilisant le format personnalisé
# df['year'] = pd.to_datetime(df['year'], format=date_format, errors='coerce')
# df['year'] = df['year'].dt.year
print(df.dtypes)


df.loc[:, 'year'] = df['year'].str.split('-').str[0]

# print(df['recclass'].value_counts())
print(type(df['geolocation'][0]))

print(df.head)
