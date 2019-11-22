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
from compute_corr import Compute_Corr

@app.callback(Output('tab-corr-graph', 'figure'),
              [Input('tab-corr-curr-dropdown', 'value'),
               Input('tab-corr-transf-dropdown', 'value'),
               Input('tab-corr-incr-radio', 'value'),
               Input('corr-year-slider', 'value')])
def tab_corr_graph(curr, transf, incr, date_range):   

    application = utils.transf2application[transf]
    t_min, t_max = utils.format_date(date_range)

    tenors = [1,2,3,6,12]

    corr_matrix, columns = Compute_Corr(
      curr, tenors, incr, transf, [t_min, t_max], application).run()

    traces = []
    #traces.append(go.Scattergl(
    #    x=[1,2,3],
    #    y=[1,2,3],
    #    mode='lines',
    #    line=dict(color='grey', width=1.),
    #))
    
    traces.append(go.Heatmap(
        z=corr_matrix,
        x=columns,
        y=columns,
    ))

    return {
        'data': traces,
        'layout': dict(
            hovermode='closest',
        )
    }

@app.callback(Output('tab-corr-slider', 'children'),
              [Input('tab-corr-curr-dropdown', 'value')])
def tab_IR_t_slider(curr):
    M = Preproc_Data(curr=curr).run()
    tenor = 1 #All tenors for a given currency have consistent date ranges.
    times = M['{}m_1d'.format(str(tenor))]['date'].values
    ti = datetime.strptime(times[-1], '%Y-%m-%d')
    tf = datetime.strptime(times[0], '%Y-%m-%d')
    t_min = 1990
    t_max = tf.year + (tf.month - 1.) / 12.
    t_list = [int(t) for t in np.arange(t_min,t_max + 0.0001,1)]
    return html.Div(
        dcc.RangeSlider(
            id='corr-year-slider',
            min=t_min,
            max=t_max,
            value=[2010, 2015],
            marks={year: str(year) for year in t_list},
            step=1./12.
        )
    )  

@app.callback(Output('tab-corr-slider-container', 'children'),
              [Input('corr-year-slider', 'value')])
def tab_IR_t_slider_container(date_range):
    t_min, t_max = utils.format_date(date_range)
    return 'Date range is "{}" -- "{}"'.format(t_min, t_max)

