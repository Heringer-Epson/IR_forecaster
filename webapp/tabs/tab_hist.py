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
        html.Div([
            dcc.Dropdown(
                id='tab-hist-curr-dropdown',
                options=[{'label': i, 'value': i} for i in ['USD', 'CAD']],
                value='USD'
            ),
            dcc.Dropdown(
                id='tab-hist-tenor-dropdown',
                options=[{'label': i, 'value': i} for i in ['1', '2', '3', '6', '12']],
                value='1'
            ),
        ],
        style={'width': '25%', 'display': 'inline-block'}),
    ]),

    html.Div([
        html.Div([
            dcc.RadioItems(
                id='tab-hist-transf-radio',
                options=[{'label': i, 'value': i} for i in ['Increment', 'Log ratio']],
                value='Increment',
                labelStyle={'display': 'inline-block'}
            ),

        ],
        style={'width': '25%', 'display': 'inline-block'}),
    ]),

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
])
