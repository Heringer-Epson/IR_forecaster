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

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))
from preprocess_data import Preproc_Data
from compute_structure import Compute_Structure

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

    merged_df = utils.merge_dataframes(M, tenors, incr, 'ir')

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
            mode='lines',
            opacity=.8,
            line=dict(width=3.),
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

