import sys
import os
import utils
import numpy as np
from dash.dependencies import Input, Output, State
import dash_html_components as html
import dash_core_components as dcc
import plotly.graph_objs as go

from server import app

sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'src'))
from preprocess_data import Preproc_Data
from forward_term import Forward_Term

N_days_max = 250

@app.callback(Output('tab-pred-graph', 'figure'),
              [Input('tab-pred-curr-dropdown', 'value'),
               Input('tab-pred-transf-dropdown', 'value'),
               Input('tab-pred-incr-radio', 'value'),
               Input('pred-year-slider', 'value'),
               Input('tab-pred-model-dropdown', 'value'),
               Input('tab-pred-distr-dropdown', 'value'),
               Input('pred-ndays-slider', 'value')],)
def tab_pred_graph(curr, transf, incr, date_range, model, distr, ndays):

    application = utils.transf2application[transf]
    IR_key = utils.transf2IR[transf]

    t_min, t_max = utils.format_date(date_range)
    M = Preproc_Data(curr=curr, incr=[int(incr)], t_ival=[t_min, t_max],
                     application=application).run()


    tenors = M['tenor'] #Using the default tenors. i.e. [1,2,3,6,12]

    merged_df = utils.merge_dataframes([M], [curr], tenors, [incr], IR_key)
    matrix = np.transpose(merged_df.values)

    paths, mean, std = Forward_Term(matrix, model, distr, N_days_max).run()
    #df = M['{}m_{}d'.format(str(tenor), incr)]
    #t_current = df['date'].values[::-1][-1] #Such that -1 index is current.


    traces = []
    
    traces.append(go.Scattergl(
        x=tenors,
        y=mean[ndays - 1],
            error_y=dict(
                type='data',
                array=std[ndays - 1],
                visible=True
            ),
        mode='lines',
        opacity=.7,
        line=dict(color='grey', width=1.),
        showlegend=False))
    
    return {
        'data': traces,
        'layout': dict(
            #xaxis={'title': t_current + '  +  t [days]',},
            xaxis={'title': 't [days]',},
            yaxis={'title': 'IR',},
            hovermode='closest',
        )}
    
@app.callback(Output('tab-pred-ndays-slider', 'children'),
              [Input('tab-pred-curr-dropdown', 'value'),
               Input('tab-pred-incr-radio', 'value')])
def tab_IR_t_slider(curr, incr):
    t_min, t_max, t_list = utils.compute_t_range(currtag=curr, incrtag=incr)

    return html.Div(
        dcc.Slider(
            id='pred-ndays-slider',
            min=1,
            max=N_days_max,
            value=1,
            marks={time: str(time) for time in np.arange(5,N_days_max + 1,25).tolist()},
            #marks={time: str(time) for time in [1,2,3,4,5]},
            step=1,
        )
    )  


@app.callback(Output('tab-pred-slider', 'children'),
              [Input('tab-pred-curr-dropdown', 'value'),
               Input('tab-pred-incr-radio', 'value')])
def tab_IR_t_slider(curr, incr):
    t_min, t_max, t_list = utils.compute_t_range(currtag=curr, incrtag=incr)

    return html.Div(
        dcc.RangeSlider(
            id='pred-year-slider',
            min=t_min,
            max=t_max,
            value=[2010, 2015],
            marks={year: str(year) for year in t_list},
            step=1./12.
        )
    )  

@app.callback(Output('tab-pred-slider-container', 'children'),
              [Input('pred-year-slider', 'value')])
def tab_IR_t_slider_container(date_range):
    t_min, t_max = utils.format_date(date_range)
    return 'Date range is "{}" -- "{}"'.format(t_min, t_max)
