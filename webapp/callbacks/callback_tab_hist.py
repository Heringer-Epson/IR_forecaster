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
from master import Master
from fit_distributions import Fit_Distr

def format_date(time_range):
    t_min = '{:04d}-{:02d}-01'.format(int(time_range[0] // 1),
                                      int(12.*(time_range[0] % 1)) + 1)
    t_max = '{:04d}-{:02d}-01'.format(int(time_range[1] // 1),
                                      int(12.*(time_range[1] % 1)) + 1)
    return t_min, t_max

@app.callback([Output('tab-hist-graph', 'figure'),
               Output('tab-hist-table', 'children')],
              [Input('tab-hist-curr-dropdown', 'value'),
               Input('tab-hist-tenor-dropdown', 'value'),
               Input('tab-hist-transf-radio', 'value'),
               Input('tab-hist-incr-radio', 'value'),
               Input('year-slider', 'value')])
def tab_hist_graph(curr, tenor, transf, incr, date_range):

    application = utils.transf2application[transf]
    M = Master(curr=curr, incr=[incr], tenor=[tenor],
               application=application).retrieve_data()
    df = M['{}m_{}d'.format(str(tenor), str(incr))]

    #Trim by date using the Slider info.
    t_min, t_max = format_date(date_range)
    t_min, t_max = format_date(date_range)
    dff = df[( (df['first_date'] >= t_min) & (df['first_date'] <= t_max) )]

    if transf == 'Raw':
        y = dff['ir_mean'].values
    else:
        y = dff['ir_transf_mean'].values
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

@app.callback(Output('tab-hist-slider-container', 'children'),
              [Input('year-slider', 'value')])
def tab_IR_t_slider_container(date_range):
    t_min, t_max = format_date(date_range)
    return 'Date range is "{}" -- "{}"'.format(t_min, t_max)

