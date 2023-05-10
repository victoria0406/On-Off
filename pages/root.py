import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

dash.register_page(__name__, path='/')

layout = html.Div([
    html.H2('Welcome to OnOff'),
    html.P('Check your phone usage')
])
