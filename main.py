import dash
from dash.dependencies import Input, Output
import dash_html_components as html
import dash_core_components as dcc
from server import app

#deploy#

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

from callbacks import cb_IR
from callbacks import cb_IRt
from callbacks import cb_hist
from callbacks import cb_term
from callbacks import cb_std
from callbacks import cb_corr
from callbacks import cb_pca
from callbacks import cb_sim
from callbacks import cb_pred

app.title = 'IR Forecaster'
app.layout = html.Div([
    #html.H1('Analysis of Intrabank Rates'),
    dcc.Tabs(id='tabs-main', value='tab-about', children=[
        dcc.Tab(label='About', value='tab-about'),
        dcc.Tab(label='Rates', value='tab-IR'),
        dcc.Tab(label='Transf. Rates', value='tab-IR_t'),
        dcc.Tab(label='Histogram', value='tab-hist'),
        dcc.Tab(label='Term Structure', value='tab-term'),
        dcc.Tab(label='Standard Dev.', value='tab-std'),
        dcc.Tab(label='Correlation Matrix', value='tab-corr'),
        dcc.Tab(label='PCA', value='tab-pca'),
        dcc.Tab(label='Simulate Rates', value='tab-sim'),
        dcc.Tab(label='Term Prediction', value='tab-pred'),
    ]),
    html.Div(id='tabs-main-content')
])

@app.callback(Output('tabs-main-content', 'children'),
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
                                
if __name__ == '__main__':
    #app.run_server(host='127.0.0.1', port=8080, debug=True)
    app.run_server(host='0.0.0.0', port=8080, debug=True)
