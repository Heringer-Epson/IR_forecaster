import dash
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import dash_html_components as html
import dash_core_components as dcc
import dash_table

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
dash_app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
dash_app.config.suppress_callback_exceptions = True
app = dash_app.server

import src.utils as utils
from src.preprocess_data import Preproc_Data
from src.fit_distributions import Fit_Distr
from src.compute_structure import Compute_Structure

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
        dcc.Tab(label='Transf. Rates', value='tab-IR_t'),
        dcc.Tab(label='Histogram', value='tab-hist'),
        dcc.Tab(label='Term Structure', value='tab-term'),
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
    elif tab == 'tab-IR_t':
        return tab_IRt.tab_IRt_layout
    elif tab == 'tab-hist':
        return tab_hist.tab_hist_layout
    elif tab == 'tab-term':
        return tab_term.tab_term_layout
    '''
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


#=-=--=-=-=-=-=-=-=-=-=-=-=-=-=-=-=TAB: IRt-=-=--=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

@dash_app.callback(Output('tab-IRt-graph', 'figure'),
              [Input('tab-IRt-curr-dropdown', 'value'),
               Input('tab-IRt-tenor-dropdown', 'value'),
               Input('tab-IRt-transf-dropdown', 'value'),
               Input('IRt-year-slider', 'value')])
def tab_IRt_graph(curr, tenor, transf, date_range):
    application = utils.transf2application[transf]
    t_min, t_max = utils.format_date(date_range)
    M = Preproc_Data(curr=curr, t_ival=[t_min, t_max],
                     application=application).run()
    df_1 = M['{}m_1d'.format(str(tenor))]
    df_25 = M['{}m_25d'.format(str(tenor))]
        
    traces = []
    traces.append(go.Scattergl(
        x=df_1['date'],
        y=df_1['ir_transf'],
        text=df_1['ir'],
        mode='lines',
        opacity=1.,
        line=dict(color='#fdae61', width=3.),
        name='T = 1 day',
    ))
    traces.append(go.Scatter(
        x=df_25['date'],
        y=df_25['ir_transf'],
        text=df_25['ir'],
        mode='lines',
        opacity=.8,
        line=dict(color='#3288bd', width=3.),
        name='T = 25 days',
    ))

    return {
        'data': traces,
        'layout': dict(
            xaxis={'title': 'Date',},
            yaxis={'title': utils.make_transf_label(transf),},
            hovermode='closest',
        )
    }

@dash_app.callback(Output('tab-IRt-slider', 'children'),
              [Input('tab-IRt-curr-dropdown', 'value'),
               Input('tab-IRt-tenor-dropdown', 'value')])
def tab_IRt_slider(curr, tenor):
    t_min, t_max, t_list = utils.compute_t_range(
      currtag=curr, tenor=[int(tenor)])
    return html.Div(
        dcc.RangeSlider(
            id='IRt-year-slider',
            min=t_min,
            max=t_max,
            value=[2010, 2015],
            marks={year: str(year) for year in t_list},
            step=1./12.
        )
    )  

@dash_app.callback(Output('tab-IRt-slider-container', 'children'),
              [Input('IRt-year-slider', 'value')])
def tab_IRt_slider_container(date_range):
    t_min, t_max = utils.format_date(date_range)
    return 'Date range is "{}" -- "{}"'.format(t_min, t_max)

#=-=--=-=-=-=-=-=-=-=-=-=-=-=-=-=-=TAB: hist-=-=--=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

@dash_app.callback([Output('tab-hist-graph', 'figure'),
               Output('tab-hist-table', 'children')],
              [Input('tab-hist-curr-dropdown', 'value'),
               Input('tab-hist-tenor-dropdown', 'value'),
               Input('tab-hist-transf-dropdown', 'value'),
               Input('tab-hist-incr-radio', 'value'),
               Input('hist-year-slider', 'value')])
def tab_hist_graph(curr, tenor, transf, incr, date_range):
    application = utils.transf2application[transf]
    IR_key = utils.transf2IR[transf]

    t_min, t_max = utils.format_date(date_range)
    M = Preproc_Data(curr=curr, incr=[int(incr)], tenor=[tenor],
                     t_ival=[t_min, t_max], application=application).run()
    df = M['{}m_{}d'.format(str(tenor), incr)]
    y = df[IR_key].values
    hist, bins, fit_dict, pdfs = Fit_Distr(y).run_fitting()
    
    traces = []
    traces.append(go.Bar(
        x=bins,
        y=hist,
        name='{} day'.format(incr),
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
    fit_df = utils.make_fit_df(fit_dict, sorted_pdfs)
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
            xaxis={'title': utils.make_transf_label(transf, incr),},
            yaxis={'title': 'Normalized count',},
            hovermode='closest',
        )}, hist_table#html.Div('Date range is "{}" -- "{}"'.format(1, 2))
    )

@dash_app.callback(Output('tab-hist-slider', 'children'),
              [Input('tab-hist-curr-dropdown', 'value'),
               Input('tab-hist-incr-radio', 'value'),
               Input('tab-hist-tenor-dropdown', 'value')])
def tab_IR_t_slider(curr, incr, tenor):
    t_min, t_max, t_list = utils.compute_t_range(
      currtag=curr, incrtag=incr, tenor=[int(tenor)])

    return html.Div(
        dcc.RangeSlider(
            id='hist-year-slider',
            min=t_min,
            max=t_max,
            value=[2010, 2015],
            marks={year: str(year) for year in t_list},
            step=1./12.
        )
    )  

@dash_app.callback(Output('tab-hist-slider-container', 'children'),
              [Input('hist-year-slider', 'value')])
def tab_IR_t_slider_container(date_range):
    t_min, t_max = utils.format_date(date_range)
    return 'Date range is "{}" -- "{}"'.format(t_min, t_max)

#=-=--=-=-=-=-=-=-=-=-=-=-=-=-=-=-=TAB: term-=-=--=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

@dash_app.callback(Output('tab-term-graph', 'figure'),
              [Input('tab-term-curr-dropdown', 'value'),
               Input('tab-term-incr-radio', 'value'),
               Input('term-year-slider', 'value')])
def tab_term_graph(curr, incr, date_range):
    
    t_min, t_max = utils.format_date(date_range)

    M = Preproc_Data(curr=curr, incr=[int(incr)], t_ival=[t_min, t_max]).run()
    tenors = M['tenor'] #Using the default tenors. i.e. [1,2,3,6,12]
    merged_df = utils.merge_dataframes([M], [curr], tenors, [incr], 'ir')

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
            mode='lines+markers',
            opacity=.8,
            line=dict(width=3.),
            marker=dict(size=10),
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

@dash_app.callback(Output('tab-term-slider', 'children'),
              [Input('tab-term-curr-dropdown', 'value'),
               Input('tab-term-incr-radio', 'value')])
def tab_term_slider(curr, incr):
    t_min, t_max, t_list = utils.compute_t_range(currtag=curr, incrtag=incr)
    return html.Div(
        dcc.RangeSlider(
            id='term-year-slider',
            min=t_min,
            max=t_max,
            value=[2010, 2015],
            marks={year: str(year) for year in t_list},
            step=1./12.
        )
    )  

@dash_app.callback(Output('tab-term-slider-container', 'children'),
              [Input('term-year-slider', 'value')])
def tab_term_slider_container(date_range):
    t_min, t_max = utils.format_date(date_range)
    return 'Date range is "{}" -- "{}"'.format(t_min, t_max)

#=-=--=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-END: TABs-=-=--=-=-=-=-=-=-=-=-=-=-=-=-=-=-
                                
if __name__ == '__main__':
    #dash_app.run_server(host='127.0.0.1', port=8080, debug=True)
    dash_app.run_server(debug=True)
