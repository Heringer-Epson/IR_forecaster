import json
import numpy as np
from dash.dependencies import Input, Output, State
import dash_html_components as html
import dash_core_components as dcc
import plotly.graph_objs as go
from server import app

import utils
from pars import Inp_Pars
from preprocess_data import Preproc_Data
from forward_term import Forward_Term

@app.callback(Output('tab-pred-intermediate-matrix', 'children'),
              [Input('tab-pred-curr-dropdown', 'value'),
               Input('tab-pred-transf-dropdown', 'value'),
               Input('tab-pred-incr-radio', 'value'),
               Input('pred-year-slider', 'value'),
               Input('tab-pred-model-dropdown', 'value'),
               Input('tab-pred-distr-radio', 'value')],)
def tab_calculate_term(curr, transf, incr, date_range, model, distr):

    application = utils.transf2application[transf]
    IR_key = utils.transf2IR[transf]

    t_min, t_max = utils.format_date(date_range)
    M = Preproc_Data(curr=curr, incr=[int(incr)], t_ival=[t_min, t_max],
                     application=application).run()

    tenors = M['tenor'] #Using the default tenors. i.e. [1,2,3,6,12]
    current_IR = utils.get_current_ir(M, tenors, incr)

    merged_df = utils.merge_dataframes([M], [curr], tenors, [incr], IR_key)
    current_date = str(merged_df.index[0])[0:10]
    matrix = np.transpose(merged_df.values)
    guess = utils.pars2guess[transf + '_' + model]
    rng_expr = utils.retrieve_rng_generators(matrix, distr)

    paths, mean, std = Forward_Term(
      matrix, model, transf, rng_expr, current_IR, guess, Inp_Pars.T_sim).run()
    out_json = [mean, std, tenors, current_date]
    return json.dumps(out_json)

@app.callback(Output('tab-pred-graph', 'figure'),
              [Input('tab-pred-intermediate-matrix', 'children'),
               Input('pred-ndays-slider', 'value')],)
def tab_pred_graph(mean_std_json, ndays):

    mean, std, tenors, current_date = json.loads(mean_std_json)
    
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
        opacity=1.,
        line=dict(color='black', width=3.),
        marker=dict(color='black', size=10),
        showlegend=False))
    
    return {
        'data': traces,
        'layout': dict(
            xaxis={'title': current_date + '  +  t [days]',},
            yaxis={'title': 'IR',},
            hovermode='closest',
        )}

#Update the distribution dropdown based on the transformation used.
#E.g. the 'Best fit' distribution can only be used with transformations that
#make the data stationary (viz. Diff. and Log ratio). 
@app.callback(
    Output('tab-pred-distr-radio', 'options'),
    [Input('tab-pred-transf-dropdown', 'value')])
def set_distr_options(transf):
    return [{'label': i, 'value': i} for i in utils.transf2distr_options[transf]]

@app.callback(
    Output('tab-pred-distr-radio', 'value'),
    [Input('tab-pred-distr-radio', 'options')])
def set_distr_value(distr_options):
    return distr_options[0]['value']
    
@app.callback(Output('tab-pred-ndays-slider', 'children'),
              [Input('tab-pred-curr-dropdown', 'value'),
               Input('tab-pred-incr-radio', 'value')])
def tab_IR_t_slider(curr, incr):
    t_min, t_max, t_list = utils.compute_t_range(currtag=curr, incrtag=incr)

    return html.Div(
        dcc.Slider(
            id='pred-ndays-slider',
            min=1,
            max=Inp_Pars.T_sim,
            value=1,
            marks={time: str(time) for time in np.arange(5,Inp_Pars.T_sim + 1,25).tolist()},
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

