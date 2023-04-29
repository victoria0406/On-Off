import dash
import dash_bootstrap_components as dbc
from dash import Input, Output, dcc, html

from themes.colors import sub_color,sub_bg_color, sub_text_color, main_color

SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": '1rem',
    "bottom": 0,
    "width": "16rem",
    "padding": "1rem",
    "background-color": sub_bg_color,
    "display": "flex",
    "flex-direction": "column",
    "justify-content": "space-between",
}
PROFILE_STYLE = {
    "background-color": "#F7F8FA",
    "height": "18rem",
    "border-radius": "5px"
}

LOGO_STYLE = {
    "color": main_color,
    "font-weight": '600',
    "text-decoration": "none",
    "font-size": "28px",
}

MENU_HEADER_STYLE = {
    "color": sub_text_color,
    "margin-top": "2rem",
    "font-size": "12px"
}

profile=html.Div([
    html.P(
        "PROFILE",
        style=MENU_HEADER_STYLE,
    ),
    html.Div([
        html.Img(
            src='./assets/user.png',
            style={'width': "14rem", "padding": "2rem 1rem 1rem"}
        ),
        html.P(
            "Domin Kim",
            style={"width": "14rem", "text-align": "center"}
        ),
        ],
        style=PROFILE_STYLE,
    )
]
)

sidebar = html.Div(
    [
        dcc.Location(id='url', refresh=False),
        html.Div([
            html.A("ON/OFF", style=LOGO_STYLE, href='/report'),
            profile,
            html.P(
                "MAIN MENU",
                style=MENU_HEADER_STYLE,
            ),
            dbc.Nav([
                dbc.NavLink('GOALS', href="/goal", active="exact"),
                dbc.NavLink('REPORTS', href="/report", active="exact"),
            ],
            vertical=True,
            pills=True,
            className='side-nav'
            )
        ]),
        html.A('LOGOUT', className='sub button'),
    ],
    style=SIDEBAR_STYLE,
)