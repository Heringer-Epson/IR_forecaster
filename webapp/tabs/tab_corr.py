import sys
import os
from dash.dependencies import Input, Output
import dash_html_components as html
import dash_core_components as dcc

tab_corr_layout = html.Div([

    html.Div([
        html.H6(
            'Correlation Matrix',
            style={'marginLeft': '3em', 'font-weight':'bold'}
        ),
        html.H6('Currency:', style={'marginLeft': '3.0em', }),
        dcc.Dropdown(
            id='tab-corr-curr-dropdown',
            options=[{'label': i, 'value': i} for i in ['USD', 'CAD', 'USD & CAD']],
            value='USD',
            style={'width': '100px', 'marginLeft': '.5em'},
        ),       
       
        html.H6('Transf.:', style={'marginLeft': '3em'}),
        dcc.Dropdown(
            id='tab-corr-transf-dropdown',
            options=[{'label': i, 'value': i} for i in ['Diff.', 'Log ratio', 'Raw']],
            value='Diff.',
            style={'width': '150px', 'marginLeft': '.5em'},
        ),        

        html.H6('Over:', style={'marginLeft': '3em'}),
        dcc.RadioItems(
            id='tab-corr-incr-radio',
            options=[{'label': '{} day'.format(i), 'value': i}
                     for i in ['1', '25', '1 & 25']],
            value='1',
        ),
        
        ], style={'display': 'flex', 'marginTop': '1.5em'}), 
        
    html.Div([dcc.Graph(id='tab-corr-graph'),], className='container'),
 
    html.Div([
        html.Div(
            id='tab-corr-slider',
            style={'width': '100%'}
            ),
    ], style={'marginBottom': 25, 'marginLeft': 100, 'marginRight': 100}),

    html.Div(
        id='tab-corr-slider-container',
        style={'textAlign': 'center'},),



])
