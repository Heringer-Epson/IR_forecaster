import sys
import os
import utils
import numpy as np
from dash.dependencies import Input, Output
import dash_html_components as html
import dash_core_components as dcc
import plotly.graph_objs as go
import dash_table

from server import app

sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'src'))
from preprocess_data import Preproc_Data
from compute_corr import Compute_Corr

@app.callback(Output('tab-corr-graph', 'figure'),
              [Input('tab-corr-curr-dropdown', 'value'),
               Input('tab-corr-transf-dropdown', 'value'),
               Input('tab-corr-incr-radio', 'value'),
               Input('corr-year-slider', 'value')])
def tab_corr_graph(currtag, transf, incrtag, date_range):   

    application = utils.transf2application[transf]
    t_min, t_max = utils.format_date(date_range)

    corr_matrix, columns = Compute_Corr(
      currtag=currtag, incrtag=incrtag, transf=transf, t_range=[t_min, t_max]).run()

    traces = []
    
    traces.append(go.Heatmap(
        z=corr_matrix,
        x=columns,
        y=columns,
        colorscale='balance',
        zmid=0,
    ))

    return {
        'data': traces,
        'layout': dict(
            hovermode='closest',
            margin = dict(r=200,l=200,t=50,b=100),
            width = 1000, height = 600,
        )
    }

@app.callback(Output('tab-corr-slider', 'children'),
              [Input('tab-corr-curr-dropdown', 'value'),
               Input('tab-corr-incr-radio', 'value')])
def tab_corr_slider(currtag, incrtag):
    t_min, t_max, t_list = utils.compute_t_range(currtag, incrtag)
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

