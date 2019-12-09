import dash
from dash.dependencies import Input, Output, State
import plotly.graph_objs as go
import dash_html_components as html
import dash_core_components as dcc
import dash_table
import numpy as np
import pandas as pd
import json

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
dash_app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
dash_app.config.suppress_callback_exceptions = True
app = dash_app.server

import src.utils as utils
from src.pars import Inp_Pars
from src.preprocess_data import Preproc_Data
from src.fit_distributions import Fit_Distr
from src.compute_structure import Compute_Structure
from src.explained_var import Explained_Var
from src.forward_term import Forward_Term
from src.compute_PCA import Compute_Pca

from tabs import tab_about
from tabs import tab_IR
from tabs import tab_IRt
from tabs import tab_std
from tabs import tab_pca
from tabs import tab_hist
from tabs import tab_term
from tabs import tab_corr
from tabs import tab_sim
from tabs import tab_pred

dash_app.title = 'IR Forecaster'
dash_app.layout = html.Div([
    dcc.Tabs(id='tabs-main', value='tab-about', children=[
        dcc.Tab(label='About', value='tab-about'),
        dcc.Tab(label='Rates', value='tab-IR'),
        dcc.Tab(label='Transf. Rates', value='tab-IR_t'),
        dcc.Tab(label='Standard Dev.', value='tab-std'),
        dcc.Tab(label='PCA', value='tab-pca'),
        dcc.Tab(label='Histogram', value='tab-hist'),
        dcc.Tab(label='Term Structure', value='tab-term'),
        dcc.Tab(label='Correlation Matrix', value='tab-corr'),
        dcc.Tab(label='Simulate Rates', value='tab-sim'),
        dcc.Tab(label='Term Prediction', value='tab-pred'),
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
    elif tab == 'tab-std':
        return tab_std.tab_std_layout
    elif tab == 'tab-pca':
        return tab_pca.tab_pca_layout
    elif tab == 'tab-hist':
        return tab_hist.tab_hist_layout
    elif tab == 'tab-term':
        return tab_term.tab_term_layout
    elif tab == 'tab-corr':
        return tab_corr.tab_corr_layout
    elif tab == 'tab-sim':
        return tab_sim.tab_sim_layout
    elif tab == 'tab-pred':
        return tab_pred.tab_pred_layout

#=-=--=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-TAB: IR-=-=--=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

@dash_app.callback(Output('tab-IR-graph', 'figure'),
              [Input('tab-IR-curr-dropdown', 'value'),
               Input('tab-IR-axis-dropdown', 'value'),
               Input('IR-year-slider', 'value'),
               Input('tab-IR-pca', 'n_clicks')])
def tab_IR_graph(curr, axis, date_range, n_clicks):

    t_min, t_max = utils.format_date(date_range)
    M = Preproc_Data(curr=curr, t_ival=[t_min, t_max]).run()
    
    merged_df = utils.merge_dataframes([M], [curr], Inp_Pars.tenor, ['1'], 'ir')
    if n_clicks % 2 == 1:
        pca = Compute_Pca(merged_df.values)#.run()
        transformed_matrix = np.transpose(pca.pca_matrix)
        y = transformed_matrix[axis]
    else:
        y = np.transpose(merged_df.values)[axis]
        
    traces = []
    traces.append(go.Scattergl(
        #x=df['date'],
        x=merged_df.index,
        y=y,
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
              [Input('tab-IR-curr-dropdown', 'value'),])
def tab_IR_slider(curr):
    t_min, t_max, t_list = utils.compute_t_range(
      currtag=curr, tenor=[1])
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

@dash_app.callback(
    Output('tab-IR-pca', 'children'),
    [Input('tab-IR-pca', 'n_clicks')])
def set_distr_options(n_clicks):
    if n_clicks % 2 == 1:
        return 'Disable PCA'
    else:
        return 'Enable PCA'

@dash_app.callback(Output('tab-IR-axis-dropdown', 'options'),
              [Input('tab-IR-pca', 'n_clicks')])
def tab_IR_axis_dropdown(n_clicks):
    if n_clicks % 2 == 1:
        return [{'label': 'PC: ' + l, 'value': i}
                for i, l in enumerate(['First', 'Second', 'Third'])]
    else:
        return [{'label': 'Tenor: ' + t + ' month', 'value': i}
                for i, t in enumerate(Inp_Pars.tenor)]

@dash_app.callback(Output('tab-IR-axis-dropdown', 'value'),
              [Input('tab-IR-pca', 'n_clicks')])
def tab_IR_axisv_dropdown(n_clicks):
    return 0

#=-=--=-=-=-=-=-=-=-=-=-=-=-=-=-=-=TAB: IRt-=-=--=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

@dash_app.callback(Output('tab-IRt-graph', 'figure'),
              [Input('tab-IRt-curr-dropdown', 'value'),
               Input('tab-IRt-axis-dropdown', 'value'),
               Input('tab-IRt-transf-dropdown', 'value'),
               Input('IRt-year-slider', 'value'),
               Input('tab-IRt-pca', 'n_clicks')])
def tab_IRt_graph(curr, axis, transf, date_range, n_clicks):
    application = utils.transf2application[transf]
    t_min, t_max = utils.format_date(date_range)
    M = Preproc_Data(curr=curr, t_ival=[t_min, t_max],
                     application=application).run()
    
    merged_df_1 = utils.merge_dataframes(
      [M], [curr], Inp_Pars.tenor, ['1'], 'ir_transf')
    merged_df_25 = utils.merge_dataframes(
      [M], [curr], Inp_Pars.tenor, ['25'], 'ir_transf')

    if n_clicks % 2 == 1:
        pca_1 = Compute_Pca(merged_df_1.values)#.run()
        transformed_matrix_1 = np.transpose(pca_1.pca_matrix)
        y_1 = transformed_matrix_1[axis]

        pca_25 = Compute_Pca(merged_df_25.values)#.run()
        transformed_matrix_25 = np.transpose(pca_25.pca_matrix)
        y_25 = transformed_matrix_25[axis]    
    
    else:
        y_1 = np.transpose(merged_df_1.values)[axis]    
        y_25 = np.transpose(merged_df_25.values)[axis]    
        
    traces = []
    traces.append(go.Scattergl(
        x=merged_df_1.index,
        y=y_1,
        mode='lines',
        opacity=1.,
        line=dict(color='#fdae61', width=3.),
        name='T = 1 day',
    ))
    traces.append(go.Scatter(
        x=merged_df_25.index,
        y=y_25,
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
              [Input('tab-IRt-curr-dropdown', 'value'),])
def tab_IRt_slider(curr):
    t_min, t_max, t_list = utils.compute_t_range(currtag=curr, tenor=[1])
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

@dash_app.callback(
    Output('tab-IRt-pca', 'children'),
    [Input('tab-IRt-pca', 'n_clicks')])
def set_distr_options(n_clicks):
    if n_clicks % 2 == 1:
        return 'Disable PCA'
    else:
        return 'Enable PCA'

@dash_app.callback(Output('tab-IRt-axis-dropdown', 'options'),
              [Input('tab-IRt-pca', 'n_clicks')])
def tab_IRt_axis_dropdown(n_clicks):
    if n_clicks % 2 == 1:
        return [{'label': 'PC: ' + l, 'value': i}
                for i, l in enumerate(['First', 'Second', 'Third'])]
    else:
        return [{'label': 'Tenor: ' + t + ' month', 'value': i}
                for i, t in enumerate(Inp_Pars.tenor)]

@dash_app.callback(Output('tab-IRt-axis-dropdown', 'value'),
              [Input('tab-IRt-pca', 'n_clicks')])
def tab_IRt_axisv_dropdown(n_clicks):
    return 0

#=-=--=-=-=-=-=-=-=-=-=-=-=-=TAB: Standard Deviation-=-=--=-=-=-=-=-=-=-=-=-=-=

@dash_app.callback(Output('tab-std-graph', 'figure'),
              [Input('tab-std-curr-dropdown', 'value'),
               Input('tab-std-transf-dropdown', 'value'),
               Input('std-year-slider', 'value'),
               Input('tab-std-pca', 'n_clicks')])
def tab_hist_graph(curr, transf, date_range, n_clicks):
    
    application = utils.transf2application[transf]
    IR_key = utils.transf2IR[transf]
    t_min, t_max = utils.format_date(date_range)

    M = Preproc_Data(
      curr=curr, t_ival=[t_min, t_max], application=application).run()
    tenors = M['tenor'] #Using the default tenors. i.e. [1,2,3,6,12]
    
    merged_df_1 = utils.merge_dataframes(
      [M], [curr], Inp_Pars.tenor, ['1'], IR_key)
    merged_df_25 = utils.merge_dataframes(
      [M], [curr], Inp_Pars.tenor, ['25'], IR_key)
    
    if n_clicks % 2 == 1:
        pca_1 = Compute_Pca(merged_df_1.values)#.run()
        transformed_matrix_1 = np.transpose(pca_1.pca_matrix)
        aux_1 = transformed_matrix_1

        pca_25 = Compute_Pca(merged_df_25.values)#.run()
        transformed_matrix_25 = np.transpose(pca_25.pca_matrix)
        aux_25 = transformed_matrix_25

        x = Inp_Pars.PCA
        y = [np.std(aux_25[i]) / np.std(aux_1[i]) for i in range(len(x))]
        x_label = 'Principal Component'

  
    else:
        aux_1 = np.transpose(merged_df_1.values)
        aux_25 = np.transpose(merged_df_25.values)
        x = Inp_Pars.tenor
        y = [np.std(aux_25[i]) / np.std(aux_1[i]) for i in range(len(x))]
        x_label = 'Maturity [months]'
    
    traces = []
    traces.append(go.Scattergl(
        x=x,
        y=y,
        mode='lines+markers',
        opacity=1.,
        line=dict(color='black', width=4.),
        marker=dict(color='black', size=10),
        showlegend=False
    ))

    return {
        'data': traces,
        'layout': dict(
            xaxis={'title': x_label,},
            yaxis={'title': r'std(T=25d) / std(T=1d)',},
            hovermode='closest',
        )
    }

@dash_app.callback(Output('tab-std-slider', 'children'),
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

@dash_app.callback(Output('tab-std-slider-container', 'children'),
              [Input('std-year-slider', 'value')])
def tab_term_slider_container(date_range):
    t_min, t_max = utils.format_date(date_range)
    return 'Date range is "{}" -- "{}"'.format(t_min, t_max)

@dash_app.callback(
    Output('tab-std-pca', 'children'),
    [Input('tab-std-pca', 'n_clicks')])
def set_distr_options(n_clicks):
    if n_clicks % 2 == 1:
        return 'Disable PCA'
    else:
        return 'Enable PCA'

#=-=--=-=-=-=-=-=-=-=-=-=-=-=-=-=-=TAB: PCA-=-=--=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

@dash_app.callback(Output('tab-pca-graph', 'figure'),
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

@dash_app.callback(Output('tab-pca-slider', 'children'),
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

@dash_app.callback(Output('tab-pca-slider-container', 'children'),
              [Input('pca-year-slider', 'value')])
def tab_IR_t_slider_container(date_range):
    t_min, t_max = utils.format_date(date_range)
    return 'Date range is "{}" -- "{}"'.format(t_min, t_max)
                
#=-=--=-=-=-=-=-=-=-=-=-=-=-=-=-=-=TAB: hist-=-=--=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

@dash_app.callback([Output('tab-hist-graph', 'figure'),
               Output('tab-hist-table', 'children')],
              [Input('tab-hist-curr-dropdown', 'value'),
               Input('tab-hist-axis-dropdown', 'value'),
               Input('tab-hist-transf-dropdown', 'value'),
               Input('tab-hist-incr-radio', 'value'),
               Input('hist-year-slider', 'value'),
               Input('tab-hist-pca', 'n_clicks')])
def tab_hist_graph(curr, axis, transf, incr, date_range, n_clicks):
    application = utils.transf2application[transf]
    IR_key = utils.transf2IR[transf]

    t_min, t_max = utils.format_date(date_range)
    M = Preproc_Data(curr=curr, incr=[int(incr)], t_ival=[t_min, t_max],
                     application=application).run()
    
    merged_df = utils.merge_dataframes(
      [M], [curr], Inp_Pars.tenor, [int(incr)], IR_key)
    if n_clicks % 2 == 1:
        pca = Compute_Pca(merged_df.values)#.run()
        transformed_matrix = np.transpose(pca.pca_matrix)
        y = transformed_matrix[axis]
    else:
        y = np.transpose(merged_df.values)[axis]

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
               Input('tab-hist-incr-radio', 'value'),])
def tab_hist_slider(curr, incr):
    t_min, t_max, t_list = utils.compute_t_range(
      currtag=curr, incrtag=incr, tenor=[1])
      
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
def tab_hist_slider_container(date_range):
    t_min, t_max = utils.format_date(date_range)
    return 'Date range is "{}" -- "{}"'.format(t_min, t_max)

@dash_app.callback(
    Output('tab-hist-pca', 'children'),
    [Input('tab-hist-pca', 'n_clicks')])
def set_distr_options(n_clicks):
    if n_clicks % 2 == 1:
        return 'Disable PCA'
    else:
        return 'Enable PCA'

@dash_app.callback(Output('tab-hist-axis-dropdown', 'options'),
              [Input('tab-hist-pca', 'n_clicks')])
def tab_hist_axis_dropdown(n_clicks):
    if n_clicks % 2 == 1:
        return [{'label': 'PC: ' + l, 'value': i}
                for i, l in enumerate(['First', 'Second', 'Third'])]
    else:
        return [{'label': 'Tenor: ' + t + ' month', 'value': i}
                for i, t in enumerate(Inp_Pars.tenor)]

@dash_app.callback(Output('tab-hist-axis-dropdown', 'value'),
              [Input('tab-hist-pca', 'n_clicks')])
def tab_hist_axisv_dropdown(n_clicks):
    return 0

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

#=-=--=-=-=-=-=-=-=-=-=-=-=-=-=-=-=TAB: corr-=-=--=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

@dash_app.callback(Output('tab-corr-graph', 'figure'),
              [Input('tab-corr-curr-dropdown', 'value'),
               Input('tab-corr-transf-dropdown', 'value'),
               Input('tab-corr-incr-radio', 'value'),
               Input('corr-year-slider', 'value'),
               Input('tab-corr-pca', 'n_clicks')])
def tab_corr_graph(currtag, transf, incrtag, date_range, n_clicks):   

    application = utils.transf2application[transf]
    t_min, t_max = utils.format_date(date_range)

    tenor_list = [1,2,3,6,12]
    IR_key = utils.transf2IR[transf]   
    curr_list = utils.currtag2curr[currtag]
    incr_list = utils.incrtag2incr[incrtag]
    M_list = [
      Preproc_Data(curr=curr, incr=incr_list, tenor=tenor_list, application=application,
        t_ival=[t_min, t_max]).run() for curr in curr_list]

    merged_df = utils.merge_dataframes(M_list, curr_list, tenor_list, incr_list, IR_key)
    columns = merged_df.columns

    if n_clicks % 2 == 1:
        pca = Compute_Pca(merged_df.values)#.run()
        columns = ['PCA 1', 'PCA 2', 'PCA 3'] #By default, always use 3 PC's.
        aux_df = pd.DataFrame(pca.pca_matrix)
        z = aux_df.corr()
    else:
        columns = merged_df.columns
        z = merged_df.corr()

    traces = []
    traces.append(go.Heatmap(
        z=z,
        x=columns,
        y=columns,
        colorscale='balance', #'curl', 'delta'
        zmid=0,
    ))

    return {
        'data': traces,
        'layout': dict(
            hovermode='closest',
            margin = dict(r=200,l=200,t=50,b=100),
            width = 1000, height = 600,
        )
    }

@dash_app.callback(Output('tab-corr-slider', 'children'),
              [Input('tab-corr-curr-dropdown', 'value'),
               Input('tab-corr-incr-radio', 'value')])
def tab_corr_slider(currtag, incrtag):
    t_min, t_max, t_list = utils.compute_t_range(currtag, incrtag)
    return html.Div(
        dcc.RangeSlider(
            id='corr-year-slider',
            min=t_min,
            max=t_max,
            value=[2010, 2015],
            marks={year: str(year) for year in t_list},
            step=1./12.
        )
    )  

@dash_app.callback(Output('tab-corr-slider-container', 'children'),
              [Input('corr-year-slider', 'value')])
def tab_IR_t_slider_container(date_range):
    t_min, t_max = utils.format_date(date_range)
    return 'Date range is "{}" -- "{}"'.format(t_min, t_max)

@dash_app.callback(
    Output('tab-corr-pca', 'children'),
    [Input('tab-corr-pca', 'n_clicks')])
def set_distr_options(n_clicks):
    if n_clicks % 2 == 1:
        return 'Disable PCA'
    else:
        return 'Enable PCA'

#=-=--=-=-=-=-=-=-=-=-=-=-=-=-=-=-TAB: Sim-=-=--=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

@dash_app.callback(Output('tab-sim-graph', 'figure'),
              [Input('tab-sim-curr-dropdown', 'value'),
               Input('tab-sim-tenor-dropdown', 'value'),
               Input('tab-sim-transf-dropdown', 'value'),
               Input('tab-sim-incr-radio', 'value'),
               Input('sim-year-slider', 'value'),
               Input('tab-sim-model-dropdown', 'value'),
               Input('tab-sim-distr-radio', 'value'),
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

    current_IR = utils.get_current_ir(M, [tenor], incr)
    merged_df = utils.merge_dataframes([M], [curr], [tenor], [incr], IR_key)

    matrix = np.transpose(merged_df.values)
    guess = utils.pars2guess[transf + '_' + model]
    rng_expr = utils.retrieve_rng_generators(matrix, distr)

    paths, mean, std = Forward_Term(
      matrix, model, transf, rng_expr, guess, ndays, npaths, current_IR, None).run()

    traces = []
    time_array = np.arange(0,ndays + 1.e-5,1)
    current_date = str(merged_df.index[0])[0:10]
    for path in paths['0']:
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
            xaxis={'title': current_date + '  +  t [days]',},
            yaxis={'title': 'IR',},
            hovermode='closest',
        )}

#Update the distribution dropdown based on the transformation used.
@dash_app.callback(
    Output('tab-sim-distr-radio', 'options'),
    [Input('tab-sim-transf-dropdown', 'value')])
def set_distr_options(transf):
    return [{'label': i, 'value': i} for i in utils.transf2distr_options[transf]]

@dash_app.callback(
    Output('tab-sim-distr-radio', 'value'),
    [Input('tab-sim-distr-radio', 'options')])
def set_distr_value(distr_options):
    return distr_options[0]['value']

@dash_app.callback(
    Output('tab-sim-transf-dropdown', 'options'),
    [Input('tab-sim-model-dropdown', 'value')])
def set_diff_options(model):
    if model == 'Brownian':
        return [{'label': i, 'value': i} for i in ['Raw']]
    elif model == 'Vasicek':
        return [{'label': i, 'value': i} for i in ['Diff.', 'Log ratio', 'Raw']]

@dash_app.callback(
    Output('tab-sim-transf-dropdown', 'value'),
    [Input('tab-sim-model-dropdown', 'value')])
def set_diff_value(model):
    return 'Raw'

@dash_app.callback(Output('tab-sim-slider', 'children'),
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

@dash_app.callback(Output('tab-sim-slider-container', 'children'),
              [Input('sim-year-slider', 'value')])
def tab_IR_t_slider_container(date_range):
    t_min, t_max = utils.format_date(date_range)
    return 'Date range is "{}" -- "{}"'.format(t_min, t_max)
    
#=-=--=-=-=-=-=-=-=-=-=-=-=-=-=-TAB: Prediction-=-=--=-=-=-=-=-=-=-=-=-=-=-=-=-

@dash_app.callback(Output('tab-pred-intermediate-matrix', 'children'),
              [Input('tab-pred-curr-dropdown', 'value'),
               Input('tab-pred-transf-dropdown', 'value'),
               Input('tab-pred-incr-radio', 'value'),
               Input('pred-year-slider', 'value'),
               Input('tab-pred-model-dropdown', 'value'),
               Input('tab-pred-distr-radio', 'value'),
               Input('tab-pred-pca', 'n_clicks')],)
def tab_calculate_term(curr, transf, incr, date_range, model, distr, n_clicks):

    application = utils.transf2application[transf]
    IR_key = utils.transf2IR[transf]

    t_min, t_max = utils.format_date(date_range)
    M = Preproc_Data(curr=curr, incr=[int(incr)], t_ival=[t_min, t_max],
                     application=application).run()

    merged_df = utils.merge_dataframes([M], [curr], Inp_Pars.tenor, [incr], IR_key)
    current_IR = utils.get_current_ir(M, Inp_Pars.tenor, incr)

    if n_clicks % 2 == 1:
        use_pca = True
    else:
        use_pca = False

    matrix = np.transpose(merged_df.values)
    current_date = str(merged_df.index[0])[0:10]
    matrix = np.transpose(merged_df.values)
    guess = utils.pars2guess[transf + '_' + model]
    rng_expr = utils.retrieve_rng_generators(matrix, distr)

    paths, mean, std = Forward_Term(
      matrix, model, transf, rng_expr, guess, Inp_Pars.T_sim,
      current_IR=current_IR, use_pca=use_pca).run()

    out_json = [mean, std, Inp_Pars.tenor, current_date]
    return json.dumps(out_json)

@dash_app.callback(Output('tab-pred-graph', 'figure'),
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
@dash_app.callback(
    Output('tab-pred-distr-radio', 'options'),
    [Input('tab-pred-transf-dropdown', 'value')])
def set_distr_options(transf):
    return [{'label': i, 'value': i} for i in utils.transf2distr_options[transf]]

@dash_app.callback(
    Output('tab-pred-distr-radio', 'value'),
    [Input('tab-pred-distr-radio', 'options')])
def set_distr_value(distr_options):
    return distr_options[0]['value']
    
@dash_app.callback(Output('tab-pred-ndays-slider', 'children'),
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

@dash_app.callback(
    Output('tab-pred-pca', 'children'),
    [Input('tab-pred-pca', 'n_clicks')])
def set_distr_options(n_clicks):
    if n_clicks % 2 == 1:
        return 'Disable PCA'
    else:
        return 'Enable PCA'

@dash_app.callback(Output('tab-pred-axis-dropdown', 'value'),
              [Input('tab-pred-pca', 'n_clicks')])
def tab_pred_axisv_dropdown(n_clicks):
    return 0

@dash_app.callback(
    Output('tab-pred-transf-dropdown', 'options'),
    [Input('tab-pred-model-dropdown', 'value')])
def set_diff_options(model):
    if model == 'Brownian':
        return [{'label': i, 'value': i} for i in ['Raw']]
    elif model == 'Vasicek':
        return [{'label': i, 'value': i} for i in ['Diff.', 'Log ratio', 'Raw']]

@dash_app.callback(
    Output('tab-pred-transf-dropdown', 'value'),
    [Input('tab-pred-model-dropdown', 'value')])
def set_diff_value(model):
    return 'Raw'

@dash_app.callback(Output('tab-pred-slider', 'children'),
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

@dash_app.callback(Output('tab-pred-slider-container', 'children'),
              [Input('pred-year-slider', 'value')])
def tab_IR_t_slider_container(date_range):
    t_min, t_max = utils.format_date(date_range)
    return 'Date range is "{}" -- "{}"'.format(t_min, t_max)

#=-=--=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-END: TABs-=-=--=-=-=-=-=-=-=-=-=-=-=-=-=-=-
                                
if __name__ == '__main__':
    #dash_app.run_server(host='0.0.0.0', port=8080, debug=False)
    dash_app.run_server(debug=True)
