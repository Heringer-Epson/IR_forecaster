import dash_html_components as html
import dash_core_components as dcc

tab_pred_layout = html.Div([
    html.Div([
        html.H6(
            'Predict Term Structure',
            style={'marginLeft': '1.5em', 'font-weight':'bold'}
        ),
       
        html.H6('Currency:', style={'marginLeft': '1.5em',}),
        dcc.Dropdown(
            id='tab-pred-curr-dropdown',
            options=[{'label': i, 'value': i} for i in ['USD', 'CAD']],
            value='USD',
            style={'width': '100px', 'marginLeft': '.5em'},
        ),       
       
        html.H6('Transf.:', style={'marginLeft': '1.5em'}),
        dcc.Dropdown(
            id='tab-pred-transf-dropdown',
            style={'width': '120px', 'marginLeft': '.5em'},
        ),        

        html.H6('Over:', style={'marginLeft': '1.5em'}),
        dcc.RadioItems(
            id='tab-pred-incr-radio',
            options=[{'label': '{} day'.format(str(i)), 'value': i} for i in ['1', '25']],
            value='1',
        ),

        html.Button(
                id='tab-pred-pca',
                children='Enable PCA',
                n_clicks=0,
                style={'width': '140px', 'marginLeft': '3em'}),   
        
        ], style={'display': 'flex', 'marginTop': '1.5em'}), 

    html.Div([
        html.H6('Model:', style={'marginLeft': '1.5em', }),
        dcc.Dropdown(
            id='tab-pred-model-dropdown',
            options=[{'label': i, 'value': i} for i in ['Vasicek', 'Brownian']],
            value='Vasicek',
            style={'width': '150px', 'marginLeft': '.5em'},
        ),       
       
        html.H6('Distribution:', style={'marginLeft': '1.5em'}),
        dcc.RadioItems(
            id='tab-pred-distr-radio',
            options=[{'label': i, 'value': i} for i in ['Best fit', 'Normal']],
            value='Best fit',
            style={'width': '75px', 'marginLeft': '.5em'},
        ),

        ], style={'display': 'flex', 'marginTop': '1.5em'}), 

    html.Div([
        dcc.Graph(id='tab-pred-graph'),
        html.Div(id='tab-pred-ndays-slider', style={'width': '40%','padding-left':'30%', 'padding-right':'30%'})
    ]),
 
    html.Div([
        html.Div(
            id='tab-pred-slider',
            style={'width': '100%'}
            ),
    ], style={'marginTop': 50, 'marginBottom': 25, 'marginLeft': 100, 'marginRight': 100}),

    html.Div(
        id='tab-pred-slider-container',
        style={'textAlign': 'center'},),
        
    #Hidden tab for expensive calculation of matrix of paths for forward days.
    html.Div(id='tab-pred-intermediate-matrix', style={'display': 'none'})
])
