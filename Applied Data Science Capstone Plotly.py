# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
df = pd.read_csv("spacex_launch_dash.csv")
max_payload = df['Payload Mass (kg)'].max()
min_payload = df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                dcc.Dropdown(id='site-dropdown',
                                             options=[
                                                         {'label': 'ALL', 'value': 'ALL'}
                                                     ] + [{'label': site, 'value': site} for site in
                                                          df['Launch Site'].unique()],
                                             value='ALL',
                                             placeholder="Select a Launch Site here",
                                             searchable=True),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                dcc.RangeSlider(id='payload-slider',
                                                min=0, max=10000, step=1000,
                                                marks={0: '0', 10000: '10000'},
                                                value=[min_payload, max_payload]),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])


# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(
    Output('success-pie-chart', 'figure'),
    Input('site-dropdown', 'value'))
def get_pie_chart(entered_site):
    if entered_site == "ALL":
        filtered_df = df
    else:
        filtered_df = df[df['Launch Site'] == entered_site]

    # Count success/failure
    pie_data = filtered_df['class'].value_counts().reset_index()
    pie_data.columns = ['class', 'count']

    # Create pie chart
    fig = px.pie(
        pie_data,
        names='class',
        values='count',
        title=f'Success vs Failure Rate for {entered_site}',
        color='class',
        color_discrete_map={0: 'red', 1: 'green'}
    )
    return fig


# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'),
              Input(component_id="payload-slider", component_property="value")
              )
def get_scatter_plot(entered_site, payload_range):
    # Filter data based on payload range
    filtered_df = df[(df['Payload Mass (kg)'] >= payload_range[0]) &
                     (df['Payload Mass (kg)'] <= payload_range[1])]

    # Filter data based on selected launch site
    if entered_site != "ALL":
        filtered_df = filtered_df[filtered_df['Launch Site'] == entered_site]

    fig = px.scatter(
        filtered_df,
        x='Payload Mass (kg)',
        y='class',
        color="Booster Version Category",
        title=f"Payload vs. Success for {entered_site}"
    )
    return fig


# Run the app
if __name__ == '__main__':
    app.run_server()
