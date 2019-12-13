from dash.dependencies import Input, Output
import dash_html_components as html
import dash_core_components as dcc

tab_pca_layout = html.Div([
    html.Div([
        html.H6(
            'PCA decomposition',
            style={'marginLeft': '1.5em', 'font-weight':'bold'}
        ),
      
        html.H6('Currency:', style={'marginLeft': '1.5em', }),
        dcc.Dropdown(
            id='tab-pca-curr-dropdown',
            options=[{'label': i, 'value': i} for i in ['USD', 'CAD']],
            value='USD',
            style={'width': '100px', 'marginLeft': '.5em'},
        ),       
       
        html.H6('Transf.:', style={'marginLeft': '1.5em'}),
        dcc.Dropdown(
            id='tab-pca-transf-dropdown',
            options=[{'label': i, 'value': i} for i in ['Diff.', 'Log ratio', 'Raw']],
            value='Raw',
            style={'width': '120px', 'marginLeft': '.5em'},
        ),        

        html.H6('Over:', style={'marginLeft': '1.5em'}),
        dcc.RadioItems(
            id='tab-pca-incr-radio',
            options=[{'label': '{} day'.format(i), 'value': i}
                     for i in ['1', '25']],
            value='1',
        ),
        
        ], style={'display': 'flex', 'marginTop': '1.5em'}), 
        
    html.Div([dcc.Graph(id='tab-pca-graph'),], className='container'),
 
    html.Div([
        html.Div(
            id='tab-pca-slider',
            style={'width': '100%'}
            ),
    ], style={'marginBottom': 25, 'marginLeft': 100, 'marginRight': 100}),

    html.Div(
        id='tab-pca-slider-container',
        style={'textAlign': 'center'},),
])
