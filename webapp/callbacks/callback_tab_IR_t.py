import sys
import os
import numpy as np
from dash.dependencies import Input, Output
import dash_html_components as html
import dash_core_components as dcc
import plotly.graph_objs as go
from datetime import datetime
import utils

from server import app

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))
from preprocess_data import Preproc_Data

@app.callback(Output('tab-IR_t-graph', 'figure'),
              [Input('tab-IR_t-curr-dropdown', 'value'),
               Input('tab-IR_t-tenor-dropdown', 'value'),
               Input('tab-IR_t-transf-radio', 'value'),
               Input('year-slider', 'value')])
def tab_IR_t_graph(curr, tenor, transf, date_range):
    application = utils.transf2application[transf]
    t_min, t_max = utils.format_date(date_range)
    M = Preproc_Data(curr=curr, t_ival=[t_min, t_max],
                     application=application).run()
    df_1 = M['{}m_1d'.format(str(tenor))]
    df_25 = M['{}m_25d'.format(str(tenor))]
        
    traces = []
    traces.append(go.Scattergl(
        x=df_1['date'],
        y=df_1['ir_transf'],
        text=df_1['ir'],
        mode='lines',
        opacity=1.,
        line=dict(color='#fdae61', width=3.),
        name='1 day',
    ))
    traces.append(go.Scatter(
        x=df_25['date'],
        y=df_25['ir_transf'],
        text=df_25['ir'],
        mode='lines',
        opacity=.8,
        line=dict(color='#3288bd', width=3.),
        name='25 days',
    ))

    return {
        'data': traces,
        'layout': dict(
            xaxis={'title': 'Date',},
            yaxis={'title': 'IR',},
            hovermode='closest',
        )
    }

@app.callback(Output('tab-IR_t-slider', 'children'),
              [Input('tab-IR_t-curr-dropdown', 'value'),
               Input('tab-IR_t-tenor-dropdown', 'value')])
def tab_IR_t_slider(curr, tenor):
    M = Preproc_Data(curr=curr).run()
    times = M['{}m_1d'.format(str(tenor))]['date'].values
    ti = datetime.strptime(times[-1], '%Y-%m-%d')
    tf = datetime.strptime(times[0], '%Y-%m-%d')
    t_min = 1990
    t_max = tf.year + (tf.month - 1.) / 12.
    t_list = [int(t) for t in np.arange(t_min,t_max + 0.0001,1)]
    return html.Div(
        dcc.RangeSlider(
            id='year-slider',
            min=t_min,
            max=t_max,
            value=[2010, 2015],
            marks={year: str(year) for year in t_list},
            step=1./12.
        )
    )  

@app.callback(Output('tab-IR_t-slider-container', 'children'),
              [Input('year-slider', 'value')])
def tab_IR_t_slider_container(date_range):
    t_min, t_max = utils.format_date(date_range)
    return 'Date range is "{}" -- "{}"'.format(t_min, t_max)

