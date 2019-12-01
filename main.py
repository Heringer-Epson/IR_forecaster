import dash
from dash.dependencies import Input, Output
import dash_html_components as html
import dash_core_components as dcc

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.config.suppress_callback_exceptions = True

from tabs import tab_about

app.title = 'IR Forecaster'
app.layout = html.Div([
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
