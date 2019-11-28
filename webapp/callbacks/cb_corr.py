import sys
import os
import numpy as np
from dash.dependencies import Input, Output
import dash_html_components as html
import dash_core_components as dcc
import plotly.graph_objs as go
from server import app

import utils
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'src'))
from preprocess_data import Preproc_Data

@app.callback(Output('tab-corr-graph', 'figure'),
              [Input('tab-corr-curr-dropdown', 'value'),
               Input('tab-corr-transf-dropdown', 'value'),
               Input('tab-corr-incr-radio', 'value'),
               Input('corr-year-slider', 'value')])
def tab_corr_graph(currtag, transf, incrtag, date_range):   

    application = utils.transf2application[transf]
    t_min, t_max = utils.format_date(date_range)

    tenor_list = [1,2,3,6,12]
    IR_key = utils.transf2IR[transf]   
    curr_list = utils.currtag2curr[currtag]
    incr_list = utils.incrtag2incr[incrtag]
    M_list = [
      Preproc_Data(curr=curr, incr=incr_list, tenor=tenor_list, application=application,
        t_ival=[t_min, t_max]).run() for curr in curr_list]

    merged_df = utils.merge_dataframes(M_list, curr_list, tenor_list, incr_list, IR_key)
    columns = merged_df.columns

    traces = []
    traces.append(go.Heatmap(
        z=merged_df.corr(),
        x=merged_df.columns,
        y=merged_df.columns,
        colorscale='balance', #'curl', 'delta'
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

