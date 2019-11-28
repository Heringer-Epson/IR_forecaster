from dash.dependencies import Input, Output
import dash_html_components as html
import dash_core_components as dcc
import plotly.graph_objs as go
from server import app

import utils
from preprocess_data import Preproc_Data
from explained_var import Explained_Var

@app.callback(Output('tab-pca-graph', 'figure'),
              [Input('tab-pca-curr-dropdown', 'value'),
               Input('tab-pca-transf-dropdown', 'value'),
               Input('tab-pca-incr-radio', 'value'),
               Input('pca-year-slider', 'value')])
def tab_pca_graph(curr, transf, incr, date_range):   

    application = utils.transf2application[transf]
    IR_key = utils.transf2IR[transf]
    t_min, t_max = utils.format_date(date_range)

    M = Preproc_Data(curr=curr, incr=[int(incr)], t_ival=[t_min, t_max],
                     application=application).run()
    
    merged_df = utils.merge_dataframes([M], [curr], M['tenor'], [incr], IR_key)    
    n_pca_array, exp_var = Explained_Var(merged_df.values).run()
    
    traces = []
    traces.append(go.Scattergl(
        x=n_pca_array,
        y=exp_var,
        mode='lines+markers',
        opacity=1.,
        line=dict(color='black', width=3.),
        marker=dict(color='black', size=10),
    ))

    return {
        'data': traces,
        'layout': dict(
            xaxis={'title': 'Number of Principal Components',},
            yaxis={'title': 'Explained Variance [%]',},
            hovermode='closest',
        )
    }

@app.callback(Output('tab-pca-slider', 'children'),
              [Input('tab-pca-curr-dropdown', 'value'),
               Input('tab-pca-incr-radio', 'value')])
def tab_corr_slider(currtag, incrtag):
    t_min, t_max, t_list = utils.compute_t_range(currtag, incrtag)
    return html.Div(
        dcc.RangeSlider(
            id='pca-year-slider',
            min=t_min,
            max=t_max,
            value=[2010, 2015],
            marks={year: str(year) for year in t_list},
            step=1./12.
        )
    )  

@app.callback(Output('tab-pca-slider-container', 'children'),
              [Input('pca-year-slider', 'value')])
def tab_IR_t_slider_container(date_range):
    t_min, t_max = utils.format_date(date_range)
    return 'Date range is "{}" -- "{}"'.format(t_min, t_max)

