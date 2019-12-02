import dash
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import dash_html_components as html
import dash_core_components as dcc

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
dash_app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
dash_app.config.suppress_callback_exceptions = True
app = dash_app.server

import src.utils as utils
from src.preprocess_data import Preproc_Data

from tabs import tab_about
from tabs import tab_IR
from tabs import tab_IRt
from tabs import tab_hist
from tabs import tab_term
from tabs import tab_std
from tabs import tab_corr
from tabs import tab_pca
from tabs import tab_sim
from tabs import tab_pred

dash_app.title = 'IR Forecaster'
dash_app.layout = html.Div([
    #html.H1('Analysis of Intrabank Rates'),
    dcc.Tabs(id='tabs-main', value='tab-about', children=[
        dcc.Tab(label='About', value='tab-about'),
        dcc.Tab(label='Rates', value='tab-IR'),
        #dcc.Tab(label='Transf. Rates', value='tab-IR_t'),
        #dcc.Tab(label='Histogram', value='tab-hist'),
        #dcc.Tab(label='Term Structure', value='tab-term'),
        #dcc.Tab(label='Standard Dev.', value='tab-std'),
        #dcc.Tab(label='Correlation Matrix', value='tab-corr'),
        #dcc.Tab(label='PCA', value='tab-pca'),
        #dcc.Tab(label='Simulate Rates', value='tab-sim'),
        #dcc.Tab(label='Term Prediction', value='tab-pred'),
    ]),
    html.Div(id='tabs-main-content')
])

@dash_app.callback(Output('tabs-main-content', 'children'),
              [Input('tabs-main', 'value')])
def render_content(tab):
    if tab == 'tab-about':
        return tab_about.tab_about_layout
    elif tab == 'tab-IR':
        return tab_IR.tab_IR_layout
    '''
    elif tab == 'tab-IR_t':
        return tab_IRt.tab_IRt_layout
    elif tab == 'tab-hist':
        return tab_hist.tab_hist_layout
    elif tab == 'tab-term':
        return tab_term.tab_term_layout
    elif tab == 'tab-std':
        return tab_std.tab_std_layout
    elif tab == 'tab-corr':
        return tab_corr.tab_corr_layout
    elif tab == 'tab-pca':
        return tab_pca.tab_pca_layout
    elif tab == 'tab-sim':
        return tab_sim.tab_sim_layout
    elif tab == 'tab-pred':
        return tab_pred.tab_pred_layout
    '''
#=-=--=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-TAB: IR-=-=--=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

@dash_app.callback(Output('tab-IR-graph', 'figure'),
              [Input('tab-IR-curr-dropdown', 'value'),
               Input('tab-IR-tenor-dropdown', 'value'),
               Input('IR-year-slider', 'value')])
def tab_IR_graph(curr, tenor, date_range):

    t_min, t_max = utils.format_date(date_range)
    M = Preproc_Data(curr=curr, t_ival=[t_min, t_max]).run()
    df = M['{}m_1d'.format(str(tenor))]
    
    traces = []
    traces.append(go.Scattergl(
        x=df['date'],
        y=df['ir'],
        text=df['ir_transf'],
        mode='lines',
        opacity=.5,
        line=dict(color='black', width=3.),
        name='1 day',
    ))

    return {
        'data': traces,
        'layout': dict(
            xaxis={'title': 'Date',},
            yaxis={'title': 'IR',},
            hovermode='closest',
        )
    }

@dash_app.callback(Output('tab-IR-slider', 'children'),
              [Input('tab-IR-curr-dropdown', 'value'),
               Input('tab-IR-tenor-dropdown', 'value')])
def tab_IR_slider(curr, tenor):
    t_min, t_max, t_list = utils.compute_t_range(
      currtag=curr, tenor=[int(tenor)])
    return html.Div(
        dcc.RangeSlider(
            id='IR-year-slider',
            min=t_min,
            max=t_max,
            value=[2010, 2015],
            marks={year: str(year) for year in t_list},
            step=1./12.
        )
    )  

@dash_app.callback(Output('tab-IR-slider-container', 'children'),
              [Input('IR-year-slider', 'value')])
def tab_IR_slider_container(date_range):
    t_min, t_max = utils.format_date(date_range)
    return 'Date range is "{}" -- "{}"'.format(t_min, t_max)


#=-=--=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-END: TABs-=-=--=-=-=-=-=-=-=-=-=-=-=-=-=-=-
                                
if __name__ == '__main__':
    dash_app.run_server(host='127.0.0.1', port=8080, debug=True)
    #dash_app.run_server(debug=True)
