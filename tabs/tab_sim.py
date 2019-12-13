import dash_html_components as html
import dash_core_components as dcc

tab_sim_layout = html.Div([
    html.Div([
        html.H6(
            'Simulate Future Rates',
            style={'marginLeft': '1.5em', 'font-weight':'bold'}
        ),
        
        html.H6('Currency:', style={'marginLeft': '1.5em',}),
        dcc.Dropdown(
            id='tab-sim-curr-dropdown',
            options=[{'label': i, 'value': i} for i in ['USD', 'CAD']],
            value='USD',
            style={'width': '100px', 'marginLeft': '.5em'},
        ),       
       
        html.H6('Tenor:', style={'marginLeft': '1.5em'}),
        dcc.Dropdown(
            id='tab-sim-tenor-dropdown',
            options=[{'label': i + ' month', 'value': i}
                     for i in ['1', '2', '3', '6', '12']],
            value='1',
            style={'width': '150px', 'marginLeft': '.5em'},
        ),

        html.H6('Transf.:', style={'marginLeft': '1.5em'}),
        dcc.Dropdown(
            id='tab-sim-transf-dropdown',
            style={'width': '120px', 'marginLeft': '.5em'},
        ),        

        html.H6('Over:', style={'marginLeft': '1.5em'}),
        dcc.RadioItems(
            id='tab-sim-incr-radio',
            options=[{'label': '{} day'.format(str(i)), 'value': i} for i in ['1', '25']],
            value='1',
        ),
        ], style={'display': 'flex', 'marginTop': '1.5em'}), 

    html.Div([
        html.H6('Model:', style={'marginLeft': '1.5em', }),
        dcc.Dropdown(
            id='tab-sim-model-dropdown',
            options=[{'label': i, 'value': i} for i in ['Vasicek', 'Brownian']],
            #value='Brownian',
            value='Vasicek',
            style={'width': '140px', 'marginLeft': '.5em'},
        ),       
       
        html.H6('Distribution:', style={'marginLeft': '1.5em'}),
        dcc.RadioItems(
            id='tab-sim-distr-radio',
            style={'width': '75px', 'marginLeft': '.5em'},
        ),

        html.H6('# Days:', style={'marginLeft': '1.5em'}),
        dcc.Dropdown(
            id='tab-sim-ndays-dropdown',
            options=[{'label': str(i), 'value': i} for i in [50, 100, 250]],
            value=50,
            style={'width': '100px', 'marginLeft': '.5em'},
        ),  

        html.H6('# Paths:', style={'marginLeft': '1.5em'}),
        dcc.Dropdown(
            id='tab-sim-npaths-dropdown',
            options=[{'label': str(i), 'value': i} for i in [5, 10, 50, 100, 500]],
            value=5,
            style={'width': '80px', 'marginLeft': '.5em'},
        ),   
        
        html.Button(
                id='tab-sim-button',
                n_clicks=0,
                children='Re-calculate',
                style={'width': '180px', 'marginLeft': '3em'}),     

        #Add button to recalculate paths.
        ], style={'display': 'flex', 'marginTop': '1.5em'}), 

    dcc.Graph(id='tab-sim-graph'),
 
    html.Div([
        html.Div(
            id='tab-sim-slider',
            style={'width': '100%'}
            ),
    ], style={'marginBottom': 25, 'marginLeft': 100, 'marginRight': 100}),

    html.Div(
        id='tab-sim-slider-container',
        style={'textAlign': 'center'},),
])
