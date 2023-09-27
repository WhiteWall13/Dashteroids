from data.get_data import *

df_api = fetch_data_from_api()
df_csv = fetch_data_from_csv()

print(clear_df(df_api))
print(clear_df(df_csv))

print(type(clear_df(df_api)["geolocation"][0]))
print(type(clear_df(df_csv)["geolocation"][0]))


print(clear_df(df_api) == clear_df(df_csv))
