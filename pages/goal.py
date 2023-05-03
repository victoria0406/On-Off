import dash
from dash import html, dcc, callback, Input, Output
from inputdata.goalsettingdata import usage_time_info, unlock_info, app_usage_info
from component.todaygoal import today_goal_not_setting


dash.register_page(__name__)


layout = html.Div(children=[
    html.Div(today_goal_not_setting, id='today-goal'),
    html.Div([], className='calander'),
], style={'display': 'flex', 'justify-content': 'space-between'})