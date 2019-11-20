import sys
import os
from dash.dependencies import Input, Output
import dash_html_components as html
import dash_core_components as dcc

sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'src'))
from master import Master

tab_hist_layout = html.Div([
    html.H3('Histogram of Intrabank Rates'),

    html.Div([
        html.H6('Currency', style={'margin-right': '1em'}),
        dcc.Dropdown(
            id='tab-hist-curr-dropdown',
            options=[{'label': i, 'value': i} for i in ['USD', 'CAD']],
            value='USD',
        ),
    ], style={'display': 'flex'}),
        
    html.Div([
        html.H6('Tenor', style={'margin-right': '1em'}),
        dcc.Dropdown(
            id='tab-hist-tenor-dropdown',
            options=[{'label': i, 'value': i} for i in ['1','2','3','6','12']],
            value='1'
        ),
    ], style={'display': 'flex'}),        
    

    html.Div([
        html.H6('Mode', style={'margin-right': '1em'}),
        dcc.RadioItems(
            id='tab-hist-transf-radio',
            options=[{'label': i, 'value': i} for i in [
              'Raw', 'Increment', 'Log ratio']],
            value='Increment',
            style={'display': 'inline-block'},
        ),
    ], style={'display': 'inline-block'}),

    html.Div([
        html.H6('Over', style={'margin-right': '1em'}),
        dcc.RadioItems(
            id='tab-hist-incr-radio',
            options=[{'label': '{} d'.format(str(i)), 'value': i} for i in [1, 25]],
            value=1,
            labelStyle={'display': 'inline-block'}
        ),

    ], style={'width': '25%', 'display': 'inline-block'}),

    dcc.Graph(id='tab-hist-graph'),
 
    html.Div([
        html.Div(
            id='tab-hist-slider',
            style={'width': '100%'}
            ),
    ], style={'marginBottom': 25, 'marginLeft': 100, 'marginRight': 100}),

    html.Div(
        id='tab-hist-slider-container',
        style={'textAlign': 'center'},),

    html.Div(
        id='tab-hist-table',
        style={'marginTop': 100, 'marginBottom': 100, 'marginLeft': 200,
               'marginRight': 200
        },
    ),

])
