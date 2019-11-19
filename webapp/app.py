import sys
import os
import dash
from dash.dependencies import Input, Output
import dash_html_components as html
import dash_core_components as dcc
from server import app

from tabs import tab_IR
from callbacks import callback_tab_1

app.layout = html.Div([
    html.H1('Analysis of Intrabank Rates'),
    dcc.Tabs(id='tabs-main', value='tab-IR', children=[
        dcc.Tab(label='IR', value='tab-IR'),
        dcc.Tab(label='Tab Two', value='tab-2-example'),
    ]),
    html.Div(id='tabs-main-content')
])

@app.callback(Output('tabs-main-content', 'children'),
              [Input('tabs-main', 'value')])
def render_content(tab):
    if tab == 'tab-IR':
        return tab_IR.tab_IR_layout
        
    elif tab == 'tab-2-example':
        return tab_IR.tab_IR_layout

if __name__ == '__main__':
    app.run_server(debug=True)
