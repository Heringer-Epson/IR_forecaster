import sys
import os
import numpy as np
from dash.dependencies import Input, Output
import dash_html_components as html
import dash_core_components as dcc
import plotly.graph_objs as go
from datetime import datetime

from server import app

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))
from master import Master

transf2application = {'Increment':'simple_diff', 'Log ratio':'log_ratio'}
def format_date(time_range):
    t_min = '{:04d}-{:02d}-01'.format(int(time_range[0] // 1),
                                      int(12.*(time_range[0] % 1)) + 1)
    t_max = '{:04d}-{:02d}-01'.format(int(time_range[1] // 1),
                                      int(12.*(time_range[1] % 1)) + 1)
    return t_min, t_max

@app.callback(Output('tab-hist-graph', 'figure'),
              [Input('tab-hist-curr-dropdown', 'value'),
               Input('tab-hist-tenor-dropdown', 'value'),
               Input('tab-hist-transf-radio', 'value'),
               Input('year-slider', 'value')])
def tab_IR_t_graph(curr, tenor, transf, date_range):

    application = transf2application[transf]
    M = Master(curr=curr, application=application).retrieve_data()
    df_1 = M['{}m_1d'.format(str(tenor))]
    df_25 = M['{}m_25d'.format(str(tenor))]

    #Trim by date using the Slider info.
    t_min, t_max = format_date(date_range)
    t_min, t_max = format_date(date_range)
    dff_1 = df_1[df_1['first_date'] >= t_min]
    dff_1 = df_1[df_1['first_date'] <= t_max]
    dff_25 = df_25[df_25['first_date'] >= t_min]
    dff_25 = df_25[df_25['first_date'] <= t_max]
    
    traces = []

    traces.append(go.Histogram(
        x=dff_1['ir_transf_mean'],
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

@app.callback(Output('tab-hist-slider', 'children'),
              [Input('tab-hist-curr-dropdown', 'value'),
               Input('tab-hist-tenor-dropdown', 'value')])
def tab_IR_t_slider(curr, tenor):
    M = Master(curr=curr).retrieve_data()
    times = M['{}m_1d'.format(str(tenor))]['first_date'].values
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

@app.callback(Output('tab-hist-slider-container', 'children'),
              [Input('year-slider', 'value')])
def tab_IR_t_slider_container(date_range):
    t_min, t_max = format_date(date_range)
    return 'Date range is "{}" -- "{}"'.format(t_min, t_max)

