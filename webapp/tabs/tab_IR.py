import sys
import os
from dash.dependencies import Input, Output
import dash_html_components as html
import dash_core_components as dcc

sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'src'))
from master import Master

tab_IR_layout = html.Div([
    html.H3('Intrabank Rates from LIBOR'),

    html.Div([
        html.Div([
            dcc.Dropdown(
                id='tab-1-curr-dropdown',
                options=[{'label': i, 'value': i} for i in ['USD', 'CAD']],
                value='USD'
            ),
            dcc.Dropdown(
                id='tab-1-tenor-dropdown',
                options=[{'label': i, 'value': i} for i in ['1', '2', '3', '6', '12']],
                value='1'
            ),
        ],
        style={'width': '25%', 'display': 'inline-block'}),
    ]),

    html.Div([
        html.Div([
            dcc.RadioItems(
                id='tab-1-transf-radio',
                options=[{'label': i, 'value': i} for i in ['Increment', 'Log ratio']],
                value='Increment',
                labelStyle={'display': 'inline-block'}
            ),

        ],
        style={'width': '25%', 'display': 'inline-block'}),
    ]),


    dcc.Graph(id='tab-1-graph'),
 
    html.Div(
        id='tab-1-slider',
        style={'width': '80%', 'horizontal-align': 'middle'}
        ),
    #Add container showing the selected date range.
    #improve slider placement.
    #html.Div(id='tab-1-slider-container'),

  
 
    
])
