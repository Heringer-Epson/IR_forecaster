import sys, os
import dash
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.config.suppress_callback_exceptions = True
