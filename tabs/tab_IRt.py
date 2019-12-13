import dash_html_components as html
import dash_core_components as dcc

tab_IRt_layout = html.Div([
    html.Div([
        html.H6(
            'Transformed Intrabank Rates',
            style={'marginLeft': '1.5em', 'font-weight':'bold'}
        ),
       
        html.H6('Currency:', style={'marginLeft': '1.5em', }),
        dcc.Dropdown(
            id='tab-IRt-curr-dropdown',
            options=[{'label': i, 'value': i} for i in ['USD', 'CAD']],
            value='USD',
            style={'width': '100px', 'marginLeft': '.5em'},
        ),       
       
        html.H6('Axis:', style={'marginLeft': '1.5em'}),
        dcc.Dropdown(
            id='tab-IRt-axis-dropdown',
            value=0,
            style={'width': '150px', 'marginLeft': '.5em'},
        ),

        html.H6('Transf.:', style={'marginLeft': '1.5em'}),
        dcc.Dropdown(
            id='tab-IRt-transf-dropdown',
            options=[{'label': i, 'value': i} for i in ['Diff.', 'Log ratio']],
            value='Diff.',
            style={'width': '120px', 'marginLeft': '.5em'},
        ),        

        html.Button(
                id='tab-IRt-pca',
                children='Enable PCA',
                n_clicks=0,
                style={'width': '140px', 'marginLeft': '3em'}),         
                
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
