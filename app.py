import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import configparser

from get_data import get_data
from maps import *
from charts import *

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
print(gdf)

# Set MapBox Token
px.set_mapbox_access_token(config['TOKEN']['mapbox_token'])
px.set_mapbox_access_token("pk.eyJ1IjoibmhtdTEzIiwiYSI6ImNsbXVvMG5zdDBncG4ya3FqOHF5ZDFqMnYifQ.gj17oeNk6Bo60vj4pHkBXQ")

# Draw Maps
# Draw Scatter Mapbox
scatter_mapbox = draw_scatter_mapbox(gdf)
# Draw Density Mapbox
density_mapbox = draw_density_mapbox(gdf)

# Draw Charts
# Draw Sum Chart
sum_chart = draw_sum_chart(df)
# Draw CumSum Chart
cumsum_chart = draw_cumsum_chart(df)

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
    dcc.Graph(id="map", style={'width': '100%', 'height': '100%'}),
    
    dcc.Dropdown(
        id='chart-type',
        options=[
            {'label': 'Sum', 'value': 'sum'},
            {'label': 'CumSum', 'value': 'cumsum'}
        ],
        value='sum'
    ),
    dcc.Graph(id="sum-chart-type", style={"width": "100%", "height": "100%"}),
    # dcc.Graph(figure=sum_chart, id="sum", style={"width": "100%", "height": "100%"}),
    # dcc.Graph(figure=cumsum_chart, id="cumsum", style={"width": "100%", "height": "100%"})
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
    

@app.callback(
    Output('sum-chart-type', 'figure'),
    Input('chart-type', 'value')
)
def update_sum(selected_sum_type):
    """
    Updates the sum chart type based on the selected chart type.

    Parameters:
        selected_sum_type (str): The selected chart type.

    Returns:
        figure: The updated sum chart type figure.
    """
    if selected_sum_type == 'sum':
        return sum_chart
    elif selected_sum_type == 'cumsum':
        return cumsum_chart



# Execute App
if __name__ == '__main__':
    app.run_server(debug=True)
