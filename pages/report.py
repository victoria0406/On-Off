import dash
from dash import html, dcc, callback, Input, Output
import dash_bootstrap_components as dbc

col_style = {
    'background-color': '#f8f9fa',
    'border-radius': '10px',
    'padding': '10px',
    'display': 'flex',
    'flex-direction': 'row',
}

button_style = {
    'font-family': 'Arial',
    'width': '100%',
    'outline': 'None',
    'background-color': '#f8f9fa',
    'font-family': 'Arial',
    'color': '#000000',
    'border': 'none'
}

dash.register_page(__name__)

layout = html.Div(children=[
    html.Div(
        dbc.Row([
            dbc.Col(
                html.H1('This is our report page')
            ),
            dbc.Col(
                html.Div(style=col_style, children=[
                            dcc.Link(dbc.Button("Compare with Others!", outline=False, style=button_style, color='primary'), href="/group", style={'width': '100%'}),
                        ])
            )
        ]),
    ),
    html.Div('''
        This is our goal report content.
    '''),

])