import dash
from dash import html, dcc, callback, Input, Output
from inputdata.goalsettingdata import usage_time_info, unlock_info, app_usage_info


dash.register_page(__name__)

layout = html.Div(children=[
    html.H1('This is our goal page'),

    html.Div(
        f"usage_time_info: {usage_time_info['hour']}h {usage_time_info['minite']}m",
        style={'display': f"{'block' if usage_time_info['checked'] else 'none'}"},
    ),
    html.Div(
        f"usage_time_info: {unlock_info['time']}times",
        style={'display': f"{'block' if unlock_info['checked'] else 'none'}"},
    ),
    html.Div(
        f"usage_time_info: {app_usage_info['hour']}h {app_usage_info['minite']}m",
        style={'display': f"{'block' if app_usage_info['checked'] else 'none'}"},
    ),

])