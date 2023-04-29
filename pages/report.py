import dash
from dash import html, dcc, callback, Input, Output
import dash_bootstrap_components as dbc

dash.register_page(__name__)

layout = html.Div(children=[
    html.Div(
        dbc.Row([
            dbc.Col(
                html.H1('This is our report page')
            ),
            dbc.Col(
                dcc.Link(html.Button("Compare with Others!"), href="/group")
            )
        ]),
    ),
    html.Div('''
        This is our goal report content.
    '''),

])