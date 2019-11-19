import sys
import os
from dash.dependencies import Input, Output
import dash_html_components as html
import dash_core_components as dcc

sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'src'))
from master import Master

tab_IR_t_layout = html.Div([
    html.H3('Transformed Intrabank Rates'),

    html.Div([
        html.Div([
            dcc.Dropdown(
                id='tab-IR_t-curr-dropdown',
                options=[{'label': i, 'value': i} for i in ['USD', 'CAD']],
                value='USD'
            ),
            dcc.Dropdown(
                id='tab-IR_t-tenor-dropdown',
                options=[{'label': i, 'value': i} for i in ['1', '2', '3', '6', '12']],
                value='1'
            ),
        ],
        style={'width': '25%', 'display': 'inline-block'}),
    ]),

    html.Div([
        html.Div([
            dcc.RadioItems(
                id='tab-IR_t-transf-radio',
                options=[{'label': i, 'value': i} for i in ['Increment', 'Log ratio']],
                value='Increment',
                labelStyle={'display': 'inline-block'}
            ),

        ],
        style={'width': '25%', 'display': 'inline-block'}),
    ]),

    dcc.Graph(id='tab-IR_t-graph'),
 
    html.Div([
        html.Div(
            id='tab-IR_t-slider',
            style={'width': '100%'}
            ),
    ], style={'marginBottom': 25, 'marginLeft': 100, 'marginRight': 100}),

    html.Div(
        id='tab-IR_t-slider-container',
        style={'textAlign': 'center'},),
])
