import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd

from callback import get_callbacks

from component.sidebar import sidebar
from themes.colors import main_color, sub_text_color, main_bg_color, sub_color


app = dash.Dash(__name__, use_pages=True, external_stylesheets=[dbc.themes.BOOTSTRAP, "assets/style.css"])

MAIN_STYLE = {
    "margin": "0, 1rem",
    "background-color": main_color,
}

CONTENT_STYLE = {
    "margin-left": "17rem",
    "margin-right": "1rem",
    "background-color": main_bg_color,
    "height": "100vh",
    "padding": "1rem",
}

HEAD_STYLE = {
    "height": "7rem",
}


app.layout = html.Div([
    sidebar,
    html.Div([
        html.Header([
            html.H3(
                'Hello Domin Kim 👋',
                style={
                    "font-weight": '600'
                }
            ),
            html.P(
                'Let’s check your phone usage this week!',
                style={'color': sub_text_color}
            )
            ],
            style=HEAD_STYLE,    
        ),
        dash.page_container
    ],
    style=CONTENT_STYLE,
    ),
],
style=MAIN_STYLE,
)

for output, input, callback in get_callbacks():
    app.callback(output, input)(callback)

if __name__ == '__main__':
    app.run_server(debug=True)