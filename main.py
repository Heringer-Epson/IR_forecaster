import sys, os
import dash
from dash.dependencies import Input, Output
import dash_html_components as html
import dash_core_components as dcc

#sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))
#import utils
#from preprocess_data import Preproc_Data
import plotly.graph_objs as go

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

from tabs import tab_about

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
        return tab_about.tab_about_layout
                       
if __name__ == '__main__':
    #app.run_server(host='127.0.0.1', port=8080, debug=True)
    #app.run_server(host='0.0.0.0', port=8080, debug=True)
    app.run_server(debug=True)
