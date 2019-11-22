import sys
import os
import utils
import numpy as np
from dash.dependencies import Input, Output
import dash_html_components as html
import dash_core_components as dcc
import plotly.graph_objs as go
import dash_table
from datetime import datetime

from server import app

sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'src'))
from preprocess_data import Preproc_Data

@app.callback(Output('tab-std-graph', 'figure'),
              [Input('tab-std-curr-dropdown', 'value'),
               Input('tab-std-transf-dropdown', 'value'),
               Input('std-year-slider', 'value')])
def tab_hist_graph(curr, transf, date_range):
    
    application = utils.transf2application[transf]
    t_min, t_max = utils.format_date(date_range)

    data_obj = Preproc_Data(curr=curr, t_ival=[t_min, t_max],
                            application=application)
    M = data_obj.run()
    tenors = data_obj.tenor #Using the default tenors. i.e. [1,2,3,6,12]
    
    if transf == 'Raw':
        key = 'ir'
    else:
        key = 'ir_transf'
    
    std_ratio = [M['{}m_25d'.format(str(t))][key].std()\
                 /M['{}m_1d'.format(str(t))][key].std()
                 for t in tenors]
    
    traces = []

    traces.append(go.Scattergl(
        x=tenors,
        y=std_ratio,
        mode='lines',
        opacity=1.,
        line=dict(color='black', width=4.),
        showlegend=False
    ))

    return {
        'data': traces,
        'layout': dict(
            xaxis={'title': 'Maturity [months]',},
            yaxis={'title': r'std(T=25d) / std(T=1d)',},
            hovermode='closest',
        )
    }

@app.callback(Output('tab-std-slider', 'children'),
              [Input('tab-std-curr-dropdown', 'value')])
def tab_term_slider(curr):
    tenor = 1 #All tenors for a given currency have consistent date ranges.
    M = Preproc_Data(curr=curr).run()
    times = M['{}m_1d'.format(str(tenor))]['date'].values
    ti = datetime.strptime(times[-1], '%Y-%m-%d')
    tf = datetime.strptime(times[0], '%Y-%m-%d')
    t_min = 1990
    t_max = tf.year + (tf.month - 1.) / 12.
    t_list = [int(t) for t in np.arange(t_min,t_max + 0.0001,1)]
    return html.Div(
        dcc.RangeSlider(
            id='std-year-slider',
            min=t_min,
            max=t_max,
            value=[2010, 2015],
            marks={year: str(year) for year in t_list},
            step=1./12.
        )
    )  

@app.callback(Output('tab-std-slider-container', 'children'),
              [Input('std-year-slider', 'value')])
def tab_term_slider_container(date_range):
    t_min, t_max = utils.format_date(date_range)
    return 'Date range is "{}" -- "{}"'.format(t_min, t_max)

