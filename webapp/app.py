import sys
import os
import dash
from dash.dependencies import Input, Output
import dash_html_components as html
import dash_core_components as dcc
from server import app

from tabs import tab_IR
from tabs import tab_IRt
from tabs import tab_hist
from tabs import tab_term

from callbacks import cb_IR
from callbacks import cb_IRt
from callbacks import cb_hist
from callbacks import cb_term

app.layout = html.Div([
    html.H1('Analysis of Intrabank Rates'),
    dcc.Tabs(id='tabs-main', value='tab-IR', children=[
        dcc.Tab(label='IR', value='tab-IR'),
        dcc.Tab(label='Transf. IR', value='tab-IR_t'),
        dcc.Tab(label='IR Hist.', value='tab-hist'),
        dcc.Tab(label='Term Str.', value='tab-term'),
    ]),
    html.Div(id='tabs-main-content')
])

@app.callback(Output('tabs-main-content', 'children'),
              [Input('tabs-main', 'value')])
def render_content(tab):
    if tab == 'tab-IR':
        return tab_IR.tab_IR_layout
    elif tab == 'tab-IR_t':
        return tab_IRt.tab_IRt_layout
    elif tab == 'tab-hist':
        return tab_hist.tab_hist_layout
    elif tab == 'tab-term':
        return tab_term.tab_term_layout

if __name__ == '__main__':
    app.run_server(debug=True)
