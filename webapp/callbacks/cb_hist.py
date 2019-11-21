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
from fit_distributions import Fit_Distr

@app.callback([Output('tab-hist-graph', 'figure'),
               Output('tab-hist-table', 'children')],
              [Input('tab-hist-curr-dropdown', 'value'),
               Input('tab-hist-tenor-dropdown', 'value'),
               Input('tab-hist-transf-radio', 'value'),
               Input('tab-hist-incr-radio', 'value'),
               Input('year-slider', 'value')])
def tab_hist_graph(curr, tenor, transf, incr, date_range):

    application = utils.transf2application[transf]

    t_min, t_max = utils.format_date(date_range)
    M = Preproc_Data(curr=curr, incr=[incr], tenor=[tenor],
                     t_ival=[t_min, t_max], application=application).run()
    df = M['{}m_{}d'.format(str(tenor), str(incr))]


    if transf == 'Raw':
        y = df['ir'].values
    else:
        y = df['ir_transf'].values
    hist, bins, fit_dict, pdfs = Fit_Distr(y).run_fitting()
    
    traces = []
    traces.append(go.Bar(
        x=bins,
        y=hist,
        name='{} day'.format(str(incr)),
    ))
    
    sorted_pdfs = utils.sort_pdfs(fit_dict, pdfs)

    #Plot top 3 pdfs.
    for pdf in sorted_pdfs[0:3]:
        traces.append(go.Scattergl(
            x=fit_dict['x'],
            y=fit_dict['y_' + pdf],
            name=pdf,
        ))

    #Make table.
    fit_df = utils.make_fit_df(fit_dict, pdfs)

    hist_table = dash_table.DataTable(
        id='table',
        columns=[{'name': i, 'id': i} for i in fit_df.columns],
        data=fit_df.to_dict('records'),
        style_cell={
            'height': 'auto',
            'minWidth': '0px', 'maxWidth': '20px',
            'whiteSpace': 'normal'
        }
    )

    return ({
        'data': traces,
        'layout': dict(
            xaxis={'title': 'Date',},
            yaxis={'title': 'IR',},
            hovermode='closest',
        )}, hist_table#html.Div('Date range is "{}" -- "{}"'.format(1, 2))
    )

@app.callback(Output('tab-hist-slider', 'children'),
              [Input('tab-hist-curr-dropdown', 'value'),
               Input('tab-hist-tenor-dropdown', 'value')])
def tab_IR_t_slider(curr, tenor):
    M = Preproc_Data(curr=curr).run()
    times = M['{}m_1d'.format(str(tenor))]['date'].values
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

@app.callback(Output('tab-hist-slider-container', 'children'),
              [Input('year-slider', 'value')])
def tab_IR_t_slider_container(date_range):
    t_min, t_max = utils.format_date(date_range)
    return 'Date range is "{}" -- "{}"'.format(t_min, t_max)

