import sys
import os
from dash.dependencies import Input, Output
import dash_html_components as html
import dash_core_components as dcc

sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'src'))
from master import Master

tab_IR_layout = html.Div([
    html.H3('Intrabank Rates from LIBOR'),
    dcc.Dropdown(
        id='page-1-dropdown',
        options=[{'label': i, 'value': i} for i in ['USD', 'CAD']],
        value='USD'
    ),

    dcc.Graph(
        id='page-1-content')
])
