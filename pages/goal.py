import dash
from dash import html, dcc, callback, Output, Input, State
from component.todaygoal import today_goal_not_setting, today_goal_setting, unlock_weekly_calendar, usage_weekly_calendar, app_weekly_calendar, today
from component.calendar import get_calendar
from component.goaldonutplot import goal_donut_plot


dash.register_page(__name__)

layout = html.Div(children=[
    html.Div(today_goal_not_setting, id='today-goal',),
    html.Div(
        get_calendar(None, None, None, today.month),
    id='calendar-container')
], style={'display': 'flex', 'justify-content': 'space-between'})

@callback(
    [Output('calendar-container', 'children'), Output('today-goal', 'children')],
    [Input('url', 'pathname'), Input('prev-calender', 'n_clicks'), Input('next-calender', 'n_clicks')],
    [State('url', 'search'), State('month-title', 'key'), State('unlock_info', 'data'), State('usage_time_info', 'data'), State('app_usage_info', 'data')],
)

def goal_higlight_callback(pathname, prev_clicks, next_clicks, search, key, unlock_info, usage_time_info, app_usage_info):
    if pathname != '/goal': return [dash.no_update, dash.no_update]
    elif search == '?setting=True?unlock': return [unlock_weekly_calendar(unlock_info), today_goal_setting(unlock_info, usage_time_info, app_usage_info, 'unlock')]
    elif search == '?setting=True?usage': return [usage_weekly_calendar(usage_time_info), today_goal_setting(unlock_info, usage_time_info, app_usage_info, 'usage')]
    elif search == '?setting=True?app': return [app_weekly_calendar(app_usage_info), today_goal_setting(unlock_info, usage_time_info, app_usage_info, 'app')]
    elif search == '?setting=True':
        return [get_calendar(unlock_info, usage_time_info, app_usage_info, int(key)), today_goal_setting(unlock_info, usage_time_info, app_usage_info)]
    elif (prev_clicks and int(key) > 1):
        return [get_calendar(unlock_info, usage_time_info, app_usage_info, int(key) -1), dash.no_update]
    elif (next_clicks and int(key) < 12):
        return [get_calendar(unlock_info, usage_time_info, app_usage_info, int(key) + 1), dash.no_update]
    else:
        return [dash.no_update, dash.no_update]