import sys, os
import dash
from dash.dependencies import Input, Output
import dash_html_components as html
import dash_core_components as dcc
import base64

#sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))
#import utils
#from preprocess_data import Preproc_Data
import plotly.graph_objs as go

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

#from tabs import tab_about

app.title = 'IR Forecaster'
app.layout = html.Div([
    #html.H1('Analysis of Intrabank Rates'),
    dcc.Tabs(id='tabs-main', value='tab-about', children=[
        dcc.Tab(label='About', value='tab-about'),
    ]),
    html.Div(id='tabs-main-content')
])

@app.callback(Output('tabs-main-content', 'children'),
              [Input('tabs-main', 'value')])
def render_content(tab):
    if tab == 'tab-about':
        return tab_about_layout

term_png = './images/term.png'
term_base64 = base64.b64encode(open(term_png, 'rb').read()).decode('ascii')

paths_png = './images/paths.png'
paths_base64 = base64.b64encode(open(paths_png, 'rb').read()).decode('ascii')

tab_about_layout = html.Div([
    
    #Header and authorship.
    html.Div([
        html.H3(
            'Simulating future intrabank rates',
            style={'font-weight':'bold'}
        ),
        html.H3(
            'v(1.0.0)',
            style={'marginLeft': '0.75em'}
        ),    
    ], style={'display': 'flex', 'marginLeft': '3em', 'marginTop': '1.5em'}),
    
    html.H6(
        'by Epson Heringer',
        style={'marginLeft': '4em', 'marginTop': '-1em', 'font-style':'italic'}
    ),

    #Body.
    #E.g. https://community.plot.ly/t/two-graphs-side-by-side/5312
    html.Div([

        html.Div([

            #Left panel.
            html.Div([
                dcc.Markdown(
                    """
                    ###### OVERVIEW
                    This web app provides interactive plotting and analytical
                    functions to facilitate the analysis
                    
                    of intrabank rates. The user may choose to work with
                    transformed rates (rate differences or
                     
                    log of rate ratios), over a daily or monthly period. Such
                    mappings typically improve the model accuracy.
                    
                    &nbsp;&nbsp;&nbsp;&nbsp;
                    
                    Future rates are estimated using a Monte Carlo simulation,
                    where random rates (or mapped rates)
                    
                    are drawn from the distributions that best fits each tenor.
                    The user may also choose which finance model
                    
                    to use to compute forward rates, noting that the correlation 
                    between tenors is taken into account.
                    
                    Finally, the user may enable the principal component analysis
                    (PCA) option to reduce the dimensionality of the data.

                    &nbsp;&nbsp;&nbsp;&nbsp;
                    
                    ###### DATA
                    The rates used here are from the London Interbank Offered
                    Rate (LIBOR). 
                    
                    Source: The Federal Bank of Saint-Louis ([FRED](https://fred.stlouisfed.org)).

                    &nbsp;&nbsp;&nbsp;&nbsp;

                    ###### TECHNICAL DETAILS
                    
                    This web app is deployed on the Google Cloud Platform
                    and is written in python 3.7, using Dash.
                    
                    Finance models are implemented via an R wrapper to call
                    the [fitsde](https://cran.r-project.org/web/packages/Sim.DiffProc/vignettes/fitsde.html)
                    routine from the  [Sim.DiffProc](https://cran.r-project.org/web/packages/Sim.DiffProc/index.html) package.
                    
                    Github source code: https://github.com/Heringer-Epson/IR_forecaster
                    """,
                    style={'marginLeft': '3em'},
                ),      
                
            ], className="six columns"),

            #Right panel.

            html.Div([
                html.Img(
                  src='data:image/png;base64,{}'.format(term_base64),
                  style={'width':'700px', 'height':'400px', 'margin':'auto'}),
                html.Img(
                    src='data:image/png;base64,{}'.format(paths_base64),
                    style={'width':'700px', 'height':'400px', 'marginTop':'-5em'}),
                dcc.Markdown(
                    """
                    Disclaimer: The author does not take responsability in
                    profits or losses occuring from the usage of this app. 
                    """
                )
            ], style={'marginTop': '-10em'}, className="six columns"),
        ], className="row")
    ])
])   
                       
if __name__ == '__main__':
    #app.run_server(host='127.0.0.1', port=8080, debug=True)
    #app.run_server(host='0.0.0.0', port=8080, debug=True)
    app.run_server(debug=True)
