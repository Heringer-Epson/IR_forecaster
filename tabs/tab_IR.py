import dash_html_components as html
import dash_core_components as dcc
from src.pars import Inp_Pars

tab_IR_layout = html.Div([
    html.Div([
        html.H6(
            'Intrabank Rates from LIBOR',
            style={'marginLeft': '3em', 'font-weight':'bold'}
        ),
     
        html.H6('Currency:', style={'marginLeft': '3.0em', }),
        dcc.Dropdown(
            id='tab-IR-curr-dropdown',
            options=[{'label': i, 'value': i} for i in Inp_Pars.curr],
            value=Inp_Pars.curr[0],
            style={'width': '100px', 'marginLeft': '.5em'},
        ),       
       
        html.H6('Axis:', style={'marginLeft': '3em'}),
        dcc.Dropdown(
            id='tab-IR-axis-dropdown',
            value=0,
            style={'width': '150px', 'marginLeft': '.5em'},
        ),

        html.Button(
                id='tab-IR-pca',
                children='Enable PCA',
                n_clicks=0,
                style={'width': '150px', 'marginLeft': '5em'}),         
        
        ], style={'display': 'flex', 'marginTop': '1.5em'}), 

    dcc.Graph(id='tab-IR-graph'),
 
    html.Div([
        html.Div(
            id='tab-IR-slider',
            style={'width': '100%'}
            ),
    ], style={'marginBottom': 25, 'marginLeft': 100, 'marginRight': 100}),

    html.Div(
        id='tab-IR-slider-container',
        style={'textAlign': 'center'},),
])
