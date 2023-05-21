import calendar
import dash
import datetime as dt
import pandas as pd
from dash import html, dcc
from inputdata.goalsettingdata import usage_time_info, unlock_info, app_usage_info
from component.todaygoal import today_goal_not_setting, get_goal_today, get_goal_state, today
from component.calendar import get_calendar


dash.register_page(__name__)

layout = html.Div(children=[
    html.Div(today_goal_not_setting, id='today-goal',),
    html.Div(
        get_calendar(today.month),
    id='calendar-container')
], style={'display': 'flex', 'justify-content': 'space-between'})