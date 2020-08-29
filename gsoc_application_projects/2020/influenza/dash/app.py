# Import required libraries
import dash
import pandas as pd
from dash.dependencies import Input, Output, State, ClientsideFunction
import dash_core_components as dcc
import dash_html_components as html
from datetime import datetime
import util
import json

import plotly.express as px

import random

# Multi-dropdown options
from config import COUNTRIES


app = dash.Dash(
    __name__, meta_tags=[{"name": "viewport", "content": "width=device-width"}]
)
server = app.server

country_options = [
    {"label": "Austria", "value": "austria"},
    {"label": "Belgium", "value": "belgium"},
    {"label": "Germany", "value": "germany"},
    {"label": "Italy", "value": "italy"},
    {"label": "Netherlands", "value": "netherlands"},
]

df = {}
for country in COUNTRIES:
    df[country] = pd.read_csv('data/final/'+country+'.csv')
    df[country] = df[country].reset_index().set_index('week')

year_disable = [True for i in range(14)]
country_years = {
                'austria': [2012+i for i in range(6)],
                'belgium': [2009+i for i in range(11)],
                'germany': [2007+i for i in range(13)],
                'italy': [2007+i for i in range(13)],
                'netherlands': [2009+i for i in range(11)],
                }
data = util.DataGateway()

app.layout = html.Div(
    [
        dcc.Store(id="aggregate_data"),
        # empty Div to trigger javascript file for graph resizing
        html.Div(id="output-clientside"),
        html.Div(
            [
                html.Div(
                    [
                        html.Img(
                            src=app.get_asset_url("shogun-logo.png"),
                            id="dart-image",
                            style={
                                "height": "auto",
                                "width": "100px",
                                "margin-bottom": "25px",
                            },
                        ),
                    ],
                    className="one-third column",
                ),
                html.Div(
                    [
                        html.Div(
                            [
                                html.H1(
                                    "Influenza Estimator",
                                    style={"margin-bottom": "0px"},
                                ),
                                html.H3(
                                    "Shogun ML", style={"margin-top": "0px"}
                                ),
                            ]
                        )
                    ],
                    className="one-half column",
                    id="title",
                ),
                html.Div(
                    [
                        html.A(
                            html.Button("Source Code", id="learn-more-button"),
                            href="https://github.com/shogun-toolbox/applications/tree/master/gsoc_application_projects/2020/influenza",
                        )
                    ],
                    className="one-third column",
                    id="button",
                ),
            ],
            id="header",
            className="row flex-display",
            style={"margin-bottom": "25px"},
        ),
        html.H3(
            "Total Number of Cases:",
            className="control_label",
        ),
        html.Div(
            [
                html.Div(
                    [html.H6(id="world_text"), html.P("World")],
                    id="world",
                    className="mini_container",
                ),
                html.Div(
                    [html.H6(id="austria_text"), html.P("Austria")],
                    id="austria",
                    className="mini_container",
                ),
                html.Div(
                    [html.H6(id="belgium_text"), html.P("Belgium")],
                    id="belgium",
                    className="mini_container",
                ),
                html.Div(
                    [html.H6(id="germany_text"),
                     html.P("Germany")],
                    id="germany",
                    className="mini_container",
                ),
                html.Div(
                    [html.H6(id="italy_text"),
                     html.P("Italy")],
                    id="italy",
                    className="mini_container",
                ),
                html.Div(
                    [html.H6(id="netherlands_text"),
                     html.P("Netherlands")],
                    id="netherlands",
                    className="mini_container",
                ),
            ],
            id="info-container",
            className="row container-display",
        ),
        html.Div(
            [dcc.Graph(id="main_graph")],
            className="pretty_container",
        ),
        html.Div(
            [
                html.Div(
                    [
                        html.P("Filter by Model:", className="control_label"),
                        dcc.RadioItems(
                            id="model_selector",
                            options=[
                                {"label": "Linear Ridge Regression ", "value": "lrr"},
                                {"label": "Random Forest Regression ", "value": "rf"},
                                {"label": "Poisson Regression ", "value": "p", "disabled":True},
                            ],
                            value="rf",
                            className="dcc_control",
                        ),
                        html.P("Filter by Country", className="control_label"),
                        dcc.RadioItems(
                            id="country_selector",
                            options=[
                                {"label": "All", "value": "all"},
                                # {"label": "Custom ", "value": "custom"},
                            ],
                            value="all",
                            labelStyle={"display": "inline-block"},
                            className="dcc_control",
                        ),
                        dcc.Dropdown(
                            id="country_names",
                            options=country_options,
                            multi=True,
                            value=COUNTRIES,
                            className="dcc_control",
                        ),
                        html.P(
                            "Select years in histogram:\n(You can only select the years for which data is available)",
                            className="control_label",
                        ),
                        dcc.Checklist(
                            id="year_selector",
                            options=[
                                {'label': str(2007+i)+'\t', 'value': str(2007+i), 'disabled':year_disable[i]} for i in range(14)
                            ],
                            value = ["2015", "2016"],
                            labelStyle={"display": "inline-block"},
                            className="dcc_control",
                        ),  
                    ],
                    className="pretty_container four columns",
                    id="cross-filter-options",
                ),
                html.Div(
                    [
                        html.Div(
                            [dcc.Graph(id="count_graph")],
                            id="countGraphContainer",
                            className="pretty_container",
                        ),
                    ],
                    id="right-column",
                    className="eight columns",
                ),
            ],
            className="row flex-display",
        ),
        html.Div(
            [   
                html.Div(
                    [dcc.Graph(id="correlation_graph")],
                    className="pretty_container four columns",
                ),
                html.Div(
                    [dcc.Graph(id="correspondence_graph")],
                    className="pretty_container eight columns",
                ),
            ],
            className="row flex-display",
        ),
    ]
)


# Create callbacks
# callback functions: Python functions that are automatically called by Dash
# whenever an input component's property changes.
app.clientside_callback(
    ClientsideFunction(namespace="clientside", function_name="resize"),
    Output("output-clientside", "children"),
    [Input("count_graph", "figure")],
)


# Radio -> multi
# Controls the multi-view component
@app.callback(Output("country_names", "value"), [Input("country_selector", "value")])
def display_type(selector):
    if selector == "all":
        return COUNTRIES
    return []

# Nothing -> main text
# Controls the tiles displaying the live influenza cases.
@app.callback(
    [
        Output("world_text", "children"),
        Output("austria_text", "children"),
        Output("belgium_text", "children"),
        Output("germany_text", "children"),
        Output("italy_text", "children"),
        Output("netherlands_text", "children"),
    ],
    [Input("year_selector", "value")],
)
def update_text(years):

    estimates = data.get_incidence()
    estimates = util.calculate_count(estimates)

    return estimates['total_count'], estimates['austria_count'], estimates['belgium_count'], estimates['germany_count'], estimates['italy_count'], estimates['netherlands_count']

# Nothing -> main graph
# Controls What is displyed on the main map
@app.callback(
    Output("main_graph", "figure"),
    [Input("year_selector", "value")],
)
def make_main_figure(years):

    estimates = data.get_incidence()
    cases = []
    for key in estimates:
        cases.append(estimates[key])

    dff = {'iso_alpha': ['AUT', 'BEL', 'DEU', 'ITA', 'NLD'],
           'cases': cases}

    fig = px.choropleth(dff, locations="iso_alpha",
                        color="cases", 
                        center={'lat': 52.5200, 'lon': 13.4050},
                        # zoom=5,
                        scope='world',
                        height=1000,
                        title='World View',
                        # hover_name="country",  # column to add to hover information
                        color_continuous_scale=px.colors.sequential.Plasma)

    return fig


#countries -> years
# Controls the list of years available
@app.callback(
    Output("year_selector", "options"),
    [
        Input("country_names", "value"),
    ],
)
def enable_years(countries):

    year_disable = [True for i in range(14)]
    for country in countries:
        for year in country_years[country]:
            year_disable[year-2007] = False
        
    print(year_disable)
    return [{'label': str(2007+i)+'\t', 'value': str(2007+i), 'disabled': year_disable[i]} for i in range(14)]



#selectors -> histogram
# Controls the histogram/bar chart
@app.callback(
    Output("count_graph", "figure"),
    [
        Input("model_selector", "value"),
        Input("country_names", "value"),
        Input("year_selector", "value"),
    ],
)
def make_histogram(model, countries, years):

    cases = {}
    for year in years:
        for country in countries:
            for index, row in df[country].iterrows():
                if(row['week'][:4] == year):
                    if(row['date'] in cases):
                        cases[row['date']] += row['estimate_'+model]
                    else:
                        cases[row['date']] = row['estimate_'+model]
    
    weeks = []
    estimates = []
    for key in cases:
        weeks.append(datetime.strptime(key, '%Y-%m-%d'))
        estimates.append(cases[key])

    estimates = [x for _, x in sorted(zip(weeks, estimates))]
    weeks.sort()

    dff = {'week': weeks, 'cases': estimates}

    fig = px.bar(dff, x='week', y='cases',
                 hover_data=['cases'], color='cases',
                 labels={'cases': 'number of Influenza cases', 'week': 'Date'},
                 title='Cases over the years',)

    return fig


#selectors -> scatterplot
# Controls the Scatterplot
@app.callback(
    Output("correlation_graph", "figure"),
    [
        Input("model_selector", "value"),
        Input("country_names", "value"),
        Input("year_selector", "value"),
    ],
)
def make_scatter(model, countries, years):

    real = {}
    cases = {}
    for year in years:
        for country in countries:
            for index, row in df[country].iterrows():
                if(row['week'][:4] == year):
                    if(row['date'] in cases):
                        cases[row['date']] += row['estimate_'+model]
                        real[row['date']] += row['incidence']
                    else:
                        cases[row['date']] = row['estimate_'+model]
                        real[row['date']] = row['incidence']
    weeks = []
    incidence = []
    estimates = []
    for key in cases:
        weeks.append(datetime.strptime(key, '%Y-%m-%d'))
        estimates.append(cases[key])
        incidence.append(real[key])

    estimates = [x for _, x in sorted(zip(weeks, estimates))]
    incidence = [x for _, x in sorted(zip(weeks, incidence))]
    weeks.sort()
    
    dff = {'week': weeks, 'cases': estimates, 'real':incidence}

    fig = px.scatter(dff, x='real', y='cases', color='real',
                 labels={'cases': 'Estimate', 'real':'Influenza cases'},
                 opacity=0.7,
                 trendline='ols',
                 title='Correlation Graph')

    return fig


#selectors -> lineplot
# Controls the Line plot
@app.callback(
    Output("correspondence_graph", "figure"),
    [
        Input("model_selector", "value"),
        Input("country_names", "value"),
        Input("year_selector", "value"),
    ],
)
def make_line(model, countries, years):

    real = {}
    cases = {}
    for year in years:
        for country in countries:
            for index, row in df[country].iterrows():
                if(row['week'][:4] == year):
                    if(row['date'] in cases):
                        cases[row['date']] += row['estimate_'+model]
                        real[row['date']] += row['incidence']
                    else:
                        cases[row['date']] = row['estimate_'+model]
                        real[row['date']] = row['incidence']
    weeks = []
    incidence = []
    estimates = []
    for key in cases:
        weeks.append(datetime.strptime(key, '%Y-%m-%d'))
        estimates.append(cases[key])
        incidence.append(real[key])

    estimates = [x for _, x in sorted(zip(weeks, estimates))]
    incidence = [x for _, x in sorted(zip(weeks, incidence))]
    weeks.sort()
    
    weeks.extend(weeks)
    category = ['Estimate' for i in range(len(estimates))]
    estimates.extend(incidence)
    category.extend(['Real' for i in range(len(incidence))])
    
    dff = {'week': weeks, 'cases': estimates, 'category': category}

    fig = px.line(dff, x='week', y='cases', color='category',
                    title='How does the model compare to the actual values?',
                    labels={'cases': 'number of Influenza cases', 'week': 'Date'})

    return fig



## REST API
server = app.server

# @server.route('/')
# def route1():
#     return jsonify({'message':'this is the first route'})

# Returns the Live influenza PREDICTED ESTIMATE numbers as a JSON file for all the countries.
@server.route('/api/v1.0/all/current/', methods=['GET'])
def get_all_current():
    ans = data.get_incidence()
    return json.dumps(ans)


# Returns older influenza PREDICTED ESTIMATE numbers as a JSON file for all the countries.
@server.route('/api/v1.0/all/weekly/estimate/<int:year>/<int:week>/', methods=['GET'])
def get_all_weekly_estimate(year, week):
    ans = {}
    week = str(year) + '-' + str(week)
    for country in COUNTRIES:
        incidence = df[country].at[week, 'estimate_rf']
        ans[country] = incidence
    return json.dumps(ans)


# Returns older influenza INCIDENCE numbers as a JSON file for all the countries.
@server.route('/api/v1.0/all/weekly/incidence/<int:year>/<int:week>/', methods=['GET'])
def get_all_weekly_incidence(year, week):
    ans = {}
    week = str(year) + '-' + str(week)
    for country in COUNTRIES:
        incidence = df[country].at[week, 'incidence']
        ans[country] = incidence
    return json.dumps(ans)




# Main
if __name__ == "__main__":
    app.run_server(host='0.0.0.0', debug=False, port=8050)
