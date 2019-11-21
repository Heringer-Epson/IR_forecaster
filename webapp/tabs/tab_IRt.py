import sys
import os
from dash.dependencies import Input, Output
import dash_html_components as html
import dash_core_components as dcc

sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'src'))
from master import Master

tab_IRt_layout = html.Div([

    html.Div([
        html.H6(
            'Transformed Intrabank Rates',
            style={'marginLeft': '3em', 'font-weight':'bold'}
        ),
        html.H6('Currency:', style={'marginLeft': '3.0em', }),
        dcc.Dropdown(
            id='tab-IRt-curr-dropdown',
            options=[{'label': i, 'value': i} for i in ['USD', 'CAD']],
            value='USD',
            style={'width': '100px', 'marginLeft': '.5em'},
        ),       
       
        html.H6('Tenor:', style={'marginLeft': '3em'}),
        dcc.Dropdown(
            id='tab-IRt-tenor-dropdown',
            options=[{'label': i + ' month', 'value': i}
                     for i in ['1', '2', '3', '6', '12']],
            value='1',
            style={'width': '150px', 'marginLeft': '.5em'},
        ),

        html.H6('Transf.:', style={'marginLeft': '3em'}),
        dcc.Dropdown(
            id='tab-IRt-transf-dropdown',
            options=[{'label': i, 'value': i} for i in ['Diff.', 'Log ratio']],
            value='Diff.',
            style={'width': '150px', 'marginLeft': '.5em'},
        ),        
        
        ], style={'display': 'flex', 'marginTop': '1.5em'}), 

    dcc.Graph(id='tab-IRt-graph'),
 
    html.Div([
        html.Div(
            id='tab-IRt-slider',
            style={'width': '100%'}
            ),
    ], style={'marginBottom': 25, 'marginLeft': 100, 'marginRight': 100}),

    html.Div(
        id='tab-IRt-slider-container',
        style={'textAlign': 'center'},),
])
