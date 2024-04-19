# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                dcc.Dropdown(id='site-dropdown',
                                                options=[
                                                    {'label': 'All Sites', 'value':'ALL'},
                                                    {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
                                                    {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'},
                                                    {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
                                                    {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'},
                                                ],
                                                value='ALL',
                                                placeholder="Select a Launch Site Here",
                                                searchable=True
                                                ),
                                html.Br(),
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),
                                html.P("Payload range (Kg):"),
                                dcc.RangeSlider(id='payload-slider', min=0, max=10000, step=1000,
                                                value=[min_payload, max_payload]),
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])


# Callback function for pie chart
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'))
def get_pie_chart(entered_site):
    if entered_site == 'ALL':
        data = spacex_df[spacex_df['class'] == 1].groupby('Launch Site').count()
        fig = px.pie(data, values='class', names=data.index,
                     title='Total Success Launches')
        return fig
    else:
        filtered_df = spacex_df[spacex_df['Launch Site'] == entered_site]
        data = filtered_df.groupby('class').count()
        fig = px.pie(data, values='Launch Site', names=data.index,
                     title='Succeeded and Failed Launches by site')
        return fig


# Callback function for scatter plot
# Callback function for scatter plot
@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
              [Input(component_id='site-dropdown', component_property='value'),
               Input(component_id="payload-slider", component_property="value")])
def get_scatter_plot(entered_site, payload_range):
    low, high = payload_range
    mask = (spacex_df['Payload Mass (kg)'] > low) & (spacex_df['Payload Mass (kg)'] < high)
    
    if entered_site == 'ALL':
        filtered_df = spacex_df[mask]  # Apply payload mask for all sites
        fig = px.scatter(filtered_df, x="Payload Mass (kg)", y="class", color="Booster Version Category",
                         title='Correlation between Payload and Success for all Sites')
    else:
        filtered_df = spacex_df[(spacex_df['Launch Site'] == entered_site) & mask]  # Apply payload mask for selected site
        fig = px.scatter(filtered_df, x="Payload Mass (kg)", y="class", color="Booster Version Category",
                         title=f'Correlation between Payload and Success for {entered_site}')
    
    return fig



# Run the app
if __name__ == '__main__':
    app.run_server()
if __name__ == '__main__':
    app.run_server()
    