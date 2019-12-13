import dash_html_components as html
import dash_core_components as dcc

tab_hist_layout = html.Div([
    html.Div([
        html.H6(
            'Histogram of Rates',
            style={'marginLeft': '1.5em', 'font-weight':'bold'}
        ),
     
        html.H6('Currency:', style={'marginLeft': '1.5em', }),
        dcc.Dropdown(
            id='tab-hist-curr-dropdown',
            options=[{'label': i, 'value': i} for i in ['USD', 'CAD']],
            value='USD',
            style={'width': '100px', 'marginLeft': '.5em'},
        ),       
       
        html.H6('Axis:', style={'marginLeft': '1.5em'}),
        dcc.Dropdown(
            id='tab-hist-axis-dropdown',
            value=0,
            style={'width': '150px', 'marginLeft': '.5em'},
        ),

        html.H6('Transf.:', style={'marginLeft': '1.5em'}),
        dcc.Dropdown(
            id='tab-hist-transf-dropdown',
            options=[{'label': i, 'value': i} for i in ['Diff.', 'Log ratio', 'Raw']],
            value='Diff.',
            style={'width': '120px', 'marginLeft': '.5em'},
        ),        

        html.H6('Over:', style={'marginLeft': '1.5em'}),
        dcc.RadioItems(
            id='tab-hist-incr-radio',
            options=[{'label': '{} day'.format(str(i)), 'value': i} for i in ['1', '25']],
            value='1',
        ),

        html.Button(
                id='tab-hist-pca',
                children='Enable PCA',
                n_clicks=0,
                style={'width': '140px', 'marginLeft': '3em'}),   
        
        ], style={'display': 'flex', 'marginTop': '1.5em'}), 

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

    html.Div(
        id='tab-hist-table',
        style={'marginTop': 100, 'marginBottom': 100, 'marginLeft': 200,
               'marginRight': 200
        },
    ),
])
