import sys
import os
import utils
import numpy as np
from dash.dependencies import Input, Output, State
import dash_html_components as html
import dash_core_components as dcc
import plotly.graph_objs as go
import dash_table

from server import app

sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'src'))
from preprocess_data import Preproc_Data
from fit_simpars import Fit_Simpars
from forward_rates import Forward_Rates

@app.callback(Output('tab-sim-graph', 'figure'),
              [Input('tab-sim-curr-dropdown', 'value'),
               Input('tab-sim-tenor-dropdown', 'value'),
               Input('tab-sim-transf-dropdown', 'value'),
               Input('tab-sim-incr-radio', 'value'),
               Input('sim-year-slider', 'value'),
               Input('tab-sim-model-dropdown', 'value'),
               Input('tab-sim-distr-dropdown', 'value'),
               Input('tab-sim-ndays-dropdown', 'value'),
               Input('tab-sim-npaths-dropdown', 'value'),
               Input('tab-sim-button', 'n_clicks')],)
def tab_sim_graph(curr, tenor, transf, incr, date_range, model, distr, ndays,
                  npaths, n_clicks):

    application = utils.transf2application[transf]
    IR_key = utils.transf2IR[transf]

    t_min, t_max = utils.format_date(date_range)
    M = Preproc_Data(curr=curr, incr=[int(incr)], tenor=[tenor],
                     t_ival=[t_min, t_max], application=application).run()
    df = M['{}m_{}d'.format(str(tenor), incr)]
    t_current = df['date'].values[::-1][-1] #Such that -1 index is current.
    X = df[IR_key].values[::-1] 
    #X = np.random.normal(0, 0.01, 1000)
    X_0 = X[-1] #Current IR is stored in the 0 element.
    
    #In the class below, add the distr option. For now, it assumes gaussian.
    fit = Fit_Simpars(X, model).run()
    print(fit)

    traces = []
    time_array = np.arange(0,ndays + 1.e-5,1)
    
    for i in range(npaths):
        path = Forward_Rates(X_0, fit, model, ndays).run()
        traces.append(go.Scattergl(
            x=time_array,
            y=path,
            mode='lines',
            opacity=.7,
            line=dict(width=1.),
            showlegend=False
        ))
    
    return {
        'data': traces,
        'layout': dict(
            xaxis={'title': t_current + '  +  t [days]',},
            yaxis={'title': 'IR',},
            hovermode='closest',
        )}
    

@app.callback(Output('tab-sim-slider', 'children'),
              [Input('tab-sim-curr-dropdown', 'value'),
               Input('tab-sim-incr-radio', 'value'),
               Input('tab-sim-tenor-dropdown', 'value')])
def tab_IR_t_slider(curr, incr, tenor):
    t_min, t_max, t_list = utils.compute_t_range(
      currtag=curr, incrtag=incr, tenor=[int(tenor)])

    return html.Div(
        dcc.RangeSlider(
            id='sim-year-slider',
            min=t_min,
            max=t_max,
            value=[2010, 2015],
            marks={year: str(year) for year in t_list},
            step=1./12.
        )
    )  

@app.callback(Output('tab-sim-slider-container', 'children'),
              [Input('sim-year-slider', 'value')])
def tab_IR_t_slider_container(date_range):
    t_min, t_max = utils.format_date(date_range)
    return 'Date range is "{}" -- "{}"'.format(t_min, t_max)

