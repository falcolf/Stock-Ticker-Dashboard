from datetime import date
import pandas as pd
import numpy as np
import plotly.offline as pyo
import plotly.graph_objects as go
import plotly.figure_factory as ff

from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

from app import app
from utils.stock_data import get_stock_data


layout = html.Div([
                
                html.H3('Coming Soon')
            ])