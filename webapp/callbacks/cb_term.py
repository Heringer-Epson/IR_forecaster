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
from compute_structure import Compute_Structure

@app.callback(Output('tab-term-graph', 'figure'),
              [Input('tab-term-curr-dropdown', 'value'),
               Input('tab-term-incr-radio', 'value'),
               Input('term-year-slider', 'value')])
def tab_term_graph(curr, incr, date_range):
    
    t_min, t_max = utils.format_date(date_range)

    M = Preproc_Data(curr=curr, incr=[int(incr)], t_ival=[t_min, t_max]).run()
    tenors = M['tenor'] #Using the default tenors. i.e. [1,2,3,6,12]
    merged_df = utils.merge_dataframes([M], [curr], tenors, [incr], 'ir')

    struct = Compute_Structure(merged_df)
    struct_monthly = struct.get_montly_avg()
    struct_yr, struct_yr_std, labels_yr = struct.get_yearly_avg()

    #Plot top 3 pdfs.
    traces = []

    for yield_avg in struct_monthly:
        traces.append(go.Scattergl(
            x=tenors,
            y=yield_avg,
            mode='lines',
            opacity=.3,
            line=dict(color='grey', width=1.),
            showlegend=False
        ))

    for (yield_avg,yield_std,label) in zip(struct_yr,struct_yr_std,labels_yr):
        traces.append(go.Scattergl(
            x=tenors,
            y=yield_avg,
            error_y=dict(
                type='data',
                array=yield_std,
                visible=True
            ),
            mode='lines+markers',
            opacity=.8,
            line=dict(width=3.),
            marker=dict(size=10),
            name=str(label),
        ))

    return {
        'data': traces,
        'layout': dict(
            xaxis={'title': 'Maturity [months]',},
            yaxis={'title': 'Mean yield [%]',},
            hovermode='closest',
        )
    }

@app.callback(Output('tab-term-slider', 'children'),
              [Input('tab-term-curr-dropdown', 'value'),
               Input('tab-term-incr-radio', 'value')])
def tab_term_slider(curr, incr):
    t_min, t_max, t_list = utils.compute_t_range(currtag=curr, incrtag=incr)
    return html.Div(
        dcc.RangeSlider(
            id='term-year-slider',
            min=t_min,
            max=t_max,
            value=[2010, 2015],
            marks={year: str(year) for year in t_list},
            step=1./12.
        )
    )  

@app.callback(Output('tab-term-slider-container', 'children'),
              [Input('term-year-slider', 'value')])
def tab_term_slider_container(date_range):
    t_min, t_max = utils.format_date(date_range)
    return 'Date range is "{}" -- "{}"'.format(t_min, t_max)

