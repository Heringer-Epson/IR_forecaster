import sys
import os
import dash
from dash.dependencies import Input, Output
import dash_html_components as html
import dash_core_components as dcc
import plotly.graph_objs as go

from tabs import tab_IR

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))
from master import Master


M = Master().retrieve_data()

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.config.suppress_callback_exceptions = True

app.layout = html.Div([
    html.H1('Dash Tabs component demo'),
    dcc.Tabs(id='tabs-example', value='tab-1-example', children=[
        dcc.Tab(label='Tab One', value='tab-1-example'),
        dcc.Tab(label='Tab Two', value='tab-2-example'),
    ]),
    html.Div(id='tabs-content-example')
])


@app.callback(Output('tabs-content-example', 'children'),
              [Input('tabs-example', 'value')])
def render_content(tab):
    if tab == 'tab-1-example':
        return tab_IR.tab_IR_layout
        
    elif tab == 'tab-2-example':
        return html.Div([
            html.H3('Tab content 2'),
            dcc.Graph(
                id='graph-2-tabs',
                figure={
                    'data': [{
                        'x': [1, 2, 3],
                        'y': [5, 10, 6],
                        'type': 'bar'
                    }]
                }
            )
        ])

#Tab_IR_dropdown
@app.callback(Output('page-1-content', 'figure'),
              [Input('page-1-dropdown', 'value')])
def page_1_dropdown(value):

    M = Master(curr=value).retrieve_data()
    dff = M['1m_1d']

    traces = []
    traces.append(go.Scatter(
        x=dff['first_date'],
        y=dff['ir_mean'],
        text=dff['ir_mean'],
        #x=[1, 2, 3],
        #y=[6, 2, 3],
        #text=['a', 'b', 'c'],
        mode='lines',
        opacity=0.7,
        #marker={
        #    'size': 15,
        #    'line': {'width': 0.5, 'color': 'white'}
        #},
    ))

    return {
        'data': traces,
        'layout': dict(
            hovermode='closest',
        )
    }

if __name__ == '__main__':
    app.run_server(debug=True)
