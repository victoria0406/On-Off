import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd

from component.sidebar import sidebar

app = dash.Dash(__name__, use_pages=True, external_stylesheets=[dbc.themes.BOOTSTRAP])

CONTENT_STYLE = {
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}


app.layout = html.Div([
    sidebar,
    html.Div([
        html.Header(
            'Hello Domin Kim!',
        ),
        dash.page_container
    ],
    style=CONTENT_STYLE,
    ),
],
)

if __name__ == '__main__':
    app.run_server(debug=True)