from dash.dependencies import Input, Output
import dash_html_components as html
import dash_core_components as dcc
import base64

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
                    functions to faciliate the analysis
                    
                    of intrabank rates. The user may choose to work with
                    transformed rates (rate differences or
                     
                    log of rate ratios), over a daily or monthly period. Such
                    mappings typically improve the model accuracy.
                    
                    &nbsp;&nbsp;&nbsp;&nbsp;
                    
                    Future rates are estimated using a Monte Carlo simulation,
                    where random rates (or mapped rates)
                    
                    are drawn from the distribution that best fits the data.
                    The user may choose which finance model
                    
                    to use to compute forward rates. The correlation between
                    tenors is taken into account and there
                    
                    is an option to use principal component analysis to reduce
                    the dimensionality of the data.

                    &nbsp;&nbsp;&nbsp;&nbsp;
                    
                    ###### DATA
                    The rates used here are from the London Interbank Offered
                    Rate (LIBOR). 
                    
                    Source: The Federal Bank of Saint-Louis ([FRED](https://fred.stlouisfed.org)).

                    &nbsp;&nbsp;&nbsp;&nbsp;

                    ###### TECHNICAL DETAILS
                    
                    This web app is deployed on the Google Cloud Plataform
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

#dcc.Markdown(
#    """
#    # This is an <h1> tag
#    """,
#    style={'marginLeft': '6em', 'text-align':'left'},
#),        
        
