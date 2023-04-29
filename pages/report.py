import dash
import dash_bootstrap_components as dbc
from dash import html, dcc, callback, Input, Output

dash.register_page(__name__)

CONTENT_STYLE = {
    "background-color": "#F7F8FA",
    "height": "18.5rem",
    "border-radius": "5px",
    "margin-bottom": '1rem',
}

SUBCONTENT_STYLE = {
    "background-color": "white",
    'width': "20rem",
    "border-radius": "5px",
    "height": "18.5rem",
    'display': 'inline-block'    
}

BUTTON_STYLE = {
  'margin' : '-4.5rem 27rem 1.5rem 0',
  'width' : '15rem',
  'float': 'right',
  'background-color': '#EBEBF0',
  'color': '#000',
  'text-align': 'center',
  'border-radius': '5px',
  'height': '40px',
  'border': 'none'
}

TOGGLE_STYLE ={
    "margin": '-4.5rem -2rem 1.5rem 0',
    "width":"27rem",
    "float":"right",
}

layout = html.Div(children=[
    html.Div([html.Div(html.A(html.Button("Compare with Others!",style=BUTTON_STYLE), href="/group")),
            html.Div(dbc.Nav([
                dbc.NavLink('DAILY', href="/goal", active="exact"),
                dbc.NavLink('WEEKLY', href="/report", active="exact"),
            ],
            className='report-nav'
        ), style=TOGGLE_STYLE)
        ],style={'display': 'inline-block','float':"right"}
    ),    
    html.Div([
        html.Div("div1", style=SUBCONTENT_STYLE),
        html.Div("div2", style=SUBCONTENT_STYLE.update({"float":"right"})),
    ], style = CONTENT_STYLE
    ),
     html.Div([
        html.Div(),
        html.Div(),
    ], style = CONTENT_STYLE
    ),
])