import sys
import os
from dash.dependencies import Input, Output
import dash_html_components as html
import dash_core_components as dcc

sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'src'))
from master import Master

tab_term_layout = html.Div([
    html.Div([
        html.H6(
            'Averaged Term Structure',
            style={'marginLeft': '3em', 'font-weight':'bold'}
        ),
        html.H6('Currency:', style={'marginLeft': '3.0em', }),
        dcc.Dropdown(
            id='tab-term-curr-dropdown',
            options=[{'label': i, 'value': i} for i in ['USD', 'CAD']],
            value='USD',
            style={'width': '100px', 'marginLeft': '.5em'},
        ),       

        html.H6('Over:', style={'marginLeft': '3em'}),
        dcc.RadioItems(
            id='tab-term-incr-radio',
            options=[{'label': '{} day'.format(str(i)), 'value': i} for i in [1, 25]],
            value=1,
        ),
        
        ], style={'display': 'flex', 'marginTop': '1.5em'}), 
    
    dcc.Graph(id='tab-term-graph'),
 
    html.Div([
        html.Div(
            id='tab-term-slider',
            style={'width': '100%'}
            ),
    ], style={'marginBottom': 25, 'marginLeft': 100, 'marginRight': 100}),

    html.Div(
        id='tab-term-slider-container',
        style={'textAlign': 'center'},),



])
