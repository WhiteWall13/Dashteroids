import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import configparser

from get_data import get_data
from maps import *

# Config parser
config = configparser.ConfigParser()
config.read('config.ini')

# Get DataFrame
df = get_data()
df = df.dropna(subset=["geolocation"])

# Create Dash App
app = dash.Dash(__name__)

# Get GeoDataFrame
gdf = get_geodf(df)
# print(gdf)

# gdf['mass'] = df['mass'].fillna(-1)
# gdf['mass'] = df['mass'].astype(float)

# Set MapBox Token
px.set_mapbox_access_token(config['TOKEN']['mapbox_token'])
px.set_mapbox_access_token("pk.eyJ1IjoibmhtdTEzIiwiYSI6ImNsbXVvMG5zdDBncG4ya3FqOHF5ZDFqMnYifQ.gj17oeNk6Bo60vj4pHkBXQ")

# Draw Maps
# Draw Scatter Mapbox
scatter_mapbox = draw_scatter_mapbox(gdf)
#Draw Density Mapbox
density_mapbox = draw_density_mapbox(gdf)

# Layout
app.layout = html.Div([
    html.H1("Dashteroids"),
    
        dcc.Dropdown(
        id='map-type',
        options=[
            {'label': 'Scatter', 'value': 'scatter'},
            {'label': 'Density', 'value': 'density'}
        ],
        value='scatter'  # Default value
    ),
    dcc.Graph(id="map", style={'width': '100%', 'height': '100%'})
])
    
@app.callback(
    Output('map', 'figure'),
    Input('map-type', 'value')
)
def update_map(selected_map_type):
    """
    Update the map figure based on the selected map type.

    Parameters:
        selected_map_type (str): The selected map type.

    Returns:
        figure: The updated map.
    """
    if selected_map_type == 'scatter':
        return scatter_mapbox
    elif selected_map_type == 'density':
        return density_mapbox

# Execute App
if __name__ == '__main__':
    app.run_server(debug=True)
