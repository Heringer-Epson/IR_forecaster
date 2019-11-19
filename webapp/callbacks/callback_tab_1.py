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

@app.callback(Output('tab-1-graph', 'figure'),
              [Input('tab-1-curr-dropdown', 'value'),
               Input('tab-1-tenor-dropdown', 'value'),
               Input('tab-1-transf-radio', 'value'),
               Input('year-slider', 'value')])
def page_1_dropdown(curr, tenor, transf, date_range):

    application = transf2application[transf]
    print(date_range[0]) ##Filter dates based on range.
    M = Master(curr=curr, application=application).retrieve_data()
    dff_1 = M['{}m_1d'.format(str(tenor))]
    dff_25 = M['{}m_25d'.format(str(tenor))]
    
    traces = []

    traces.append(go.Scattergl(
        x=dff_1['first_date'],
        y=dff_1['ir_mean'],
        text=dff_1['ir_mean'],
        mode='lines',
        opacity=.5,
        line=dict(color='#fdae61', width=2.),
        name='1 day',
    ))
    traces.append(go.Scatter(
        x=dff_25['first_date'],
        y=dff_25['ir_mean'],
        text=dff_25['ir_mean'],
        mode='lines',
        opacity=1.,
        line=dict(color='#3288bd', width=4.),
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

@app.callback(Output('tab-1-slider', 'children'),
              [Input('tab-1-curr-dropdown', 'value'),
               Input('tab-1-tenor-dropdown', 'value')])
def tab_1_slider(curr, tenor):
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


