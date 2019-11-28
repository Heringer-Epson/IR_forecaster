import numpy as np
from dash.dependencies import Input, Output
import dash_html_components as html
import dash_core_components as dcc
import plotly.graph_objs as go
from server import app

import utils
from preprocess_data import Preproc_Data

@app.callback(Output('tab-std-graph', 'figure'),
              [Input('tab-std-curr-dropdown', 'value'),
               Input('tab-std-transf-dropdown', 'value'),
               Input('std-year-slider', 'value')])
def tab_hist_graph(curr, transf, date_range):
    
    application = utils.transf2application[transf]
    IR_key = utils.transf2IR[transf]
    t_min, t_max = utils.format_date(date_range)

    M = Preproc_Data(
      curr=curr, t_ival=[t_min, t_max], application=application).run()
    tenors = M['tenor'] #Using the default tenors. i.e. [1,2,3,6,12]
    
    std_ratio = [M['{}m_25d'.format(str(t))][IR_key].std()\
                 /M['{}m_1d'.format(str(t))][IR_key].std()
                 for t in tenors]
    
    traces = []
    traces.append(go.Scattergl(
        x=tenors,
        y=std_ratio,
        mode='lines+markers',
        opacity=1.,
        line=dict(color='black', width=4.),
        marker=dict(color='black', size=10),
        showlegend=False
    ))

    return {
        'data': traces,
        'layout': dict(
            xaxis={'title': 'Maturity [months]',},
            yaxis={'title': r'std(T=25d) / std(T=1d)',},
            hovermode='closest',
        )
    }

@app.callback(Output('tab-std-slider', 'children'),
              [Input('tab-std-curr-dropdown', 'value')])
def tab_term_slider(curr):
    t_min, t_max, t_list = utils.compute_t_range(currtag=curr)
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
