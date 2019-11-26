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

@app.callback(Output('tab-pred-graph', 'figure'),
              [Input('tab-pred-curr-dropdown', 'value'),
               Input('tab-pred-transf-dropdown', 'value'),
               Input('tab-pred-incr-radio', 'value'),
               Input('pred-year-slider', 'value'),
               Input('tab-pred-model-dropdown', 'value'),
               Input('tab-pred-distr-dropdown', 'value'),
               Input('tab-pred-ndays-dropdown', 'value')],)
def tab_pred_graph(curr, transf, incr, date_range, model, distr, ndays):

    application = utils.transf2application[transf]
    IR_key = utils.transf2IR[transf]

    t_min, t_max = utils.format_date(date_range)
    M = Preproc_Data(curr=curr, incr=[int(incr)], t_ival=[t_min, t_max],
                     application=application).run()


    tenors = M['tenor'] #Using the default tenors. i.e. [1,2,3,6,12]

    merged_df = utils.merge_dataframes([M], [curr], tenors, [incr], IR_key)
    matrix = np.transpose(merged_df.values)

    Forward_Term(matrix, model, distr, ndays).run()
    #df = M['{}m_{}d'.format(str(tenor), incr)]
    #t_current = df['date'].values[::-1][-1] #Such that -1 index is current.
    #X = df[IR_key].values[::-1] 
    #X = np.random.normal(0, 0.01, 1000)
    #X_0 = X[-1] #Current IR is stored in the 0 element.
    
    #In the class below, add the distr option. For now, it assumes gaussian.
    #fit = Fit_Simpars(X, model).run()
    #print(fit)

    traces = []
    #time_array = np.arange(0,ndays + 1.e-5,1)
    
    traces.append(go.Scattergl(
        x=[1,2,3],
        y=[1,4,9],
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

