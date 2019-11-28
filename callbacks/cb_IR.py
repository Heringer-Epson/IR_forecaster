from dash.dependencies import Input, Output
import dash_html_components as html
import dash_core_components as dcc
import plotly.graph_objs as go
from server import app

import utils
from preprocess_data import Preproc_Data

@app.callback(Output('tab-IR-graph', 'figure'),
              [Input('tab-IR-curr-dropdown', 'value'),
               Input('tab-IR-tenor-dropdown', 'value'),
               Input('IR-year-slider', 'value')])
def tab_IR_graph(curr, tenor, date_range):

    t_min, t_max = utils.format_date(date_range)
    M = Preproc_Data(curr=curr, t_ival=[t_min, t_max]).run()
    df = M['{}m_1d'.format(str(tenor))]
    
    traces = []
    traces.append(go.Scattergl(
        x=df['date'],
        y=df['ir'],
        text=df['ir_transf'],
        mode='lines',
        opacity=.5,
        line=dict(color='black', width=3.),
        name='1 day',
    ))

    return {
        'data': traces,
        'layout': dict(
            xaxis={'title': 'Date',},
            yaxis={'title': 'IR',},
            hovermode='closest',
        )
    }

@app.callback(Output('tab-IR-slider', 'children'),
              [Input('tab-IR-curr-dropdown', 'value'),
               Input('tab-IR-tenor-dropdown', 'value')])
def tab_IR_slider(curr, tenor):
    t_min, t_max, t_list = utils.compute_t_range(
      currtag=curr, tenor=[int(tenor)])
    return html.Div(
        dcc.RangeSlider(
            id='IR-year-slider',
            min=t_min,
            max=t_max,
            value=[2010, 2015],
            marks={year: str(year) for year in t_list},
            step=1./12.
        )
    )  

@app.callback(Output('tab-IR-slider-container', 'children'),
              [Input('IR-year-slider', 'value')])
def tab_IR_slider_container(date_range):
    t_min, t_max = utils.format_date(date_range)
    return 'Date range is "{}" -- "{}"'.format(t_min, t_max)

