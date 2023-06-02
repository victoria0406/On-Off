import dash
from dash import html, dcc
import dash_bootstrap_components as dbc

from flask import redirect

from callback import get_callbacks

from component.sidebar import sidebar
from inputdata.goalsettingdata import usage_time_info, unlock_info, app_usage_info
# from themes.colors import main_color, sub_text_color, main_bg_color, sub_color

app = dash.Dash(__name__, use_pages=True, external_stylesheets=[dbc.themes.BOOTSTRAP, "assets/style.css"])
server = app.server

HEAD_STYLE = {
    "height": "6.5rem",
}

app.layout = html.Div([
    dcc.Store(id = "usage_time_info", data=usage_time_info),
    dcc.Store(id = "unlock_info", data=unlock_info),
    dcc.Store(id = "app_usage_info", data=app_usage_info),
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
                style={'color': "#636363"},
                id='header-mention'
            )
            ],
            style=HEAD_STYLE,    
        ),
        dash.page_container
    ],
    className='content',
    ),
],
className='main-container',
)

server = app.server

for callback, *arcs  in get_callbacks():
    app.callback(*arcs)(callback)  

if __name__ == '__main__':
    app.run_server(debug=True)
