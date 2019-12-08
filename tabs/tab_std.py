import dash_html_components as html
import dash_core_components as dcc

tab_std_layout = html.Div([
    html.Div([
        html.H6(
            'Averaged Term Structure',
            style={'marginLeft': '3em', 'font-weight':'bold'}
        ),
       
        html.H6('Currency:', style={'marginLeft': '3.0em', }),
        dcc.Dropdown(
            id='tab-std-curr-dropdown',
            options=[{'label': i, 'value': i} for i in ['USD', 'CAD']],
            value='USD',
            style={'width': '100px', 'marginLeft': '.5em'},
        ),       

        html.H6('Transf.:', style={'marginLeft': '3em'}),
        dcc.Dropdown(
            id='tab-std-transf-dropdown',
            options=[{'label': i, 'value': i} for i in ['Diff.', 'Log ratio', 'Raw']],
            value='Diff.',
            style={'width': '150px', 'marginLeft': '.5em'},
        ),    

        html.Button(
                id='tab-std-pca',
                children='Enable PCA',
                n_clicks=0,
                style={'width': '150px', 'marginLeft': '5em'}),   
        
        ], style={'display': 'flex', 'marginTop': '1.5em'}), 
    
    dcc.Graph(id='tab-std-graph'),
 
    html.Div([
        html.Div(
            id='tab-std-slider',
            style={'width': '100%'}
            ),
    ], style={'marginBottom': 25, 'marginLeft': 100, 'marginRight': 100}),

    html.Div(
        id='tab-std-slider-container',
        style={'textAlign': 'center'},),



])
