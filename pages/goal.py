import dash
from dash import html, dcc, callback, Output, Input, State
from inputdata.goalsettingdata import usage_time_info, unlock_info, app_usage_info
from component.todaygoal import today_goal_not_setting, today_goal_setting, today_goal_donut_plot, unlock_weekly_calendar, usage_weekly_calendar, app_weekly_calendar, today
from component.calendar import get_calendar


dash.register_page(__name__)

layout = html.Div(children=[
    html.Div(today_goal_not_setting, id='today-goal',),
    html.Div(
        get_calendar(today.month),
    id='calendar-container')
], style={'display': 'flex', 'justify-content': 'space-between'})

@callback(
    [Output('calendar-container', 'children'), Output('today-goal', 'children'), Output('today-goal-status', 'children')],
    [Input('url', 'pathname'), Input('prev-calender', 'n_clicks'), Input('next-calender', 'n_clicks')],
    [State('url', 'search'), State('month-title', 'key')],
)

def goal_higlight_callback(pathname, prev_clicks, next_clicks, search, key):
    if pathname != '/goal': return [dash.no_update, dash.no_update]
    elif search == '?setting=True?unlock': return [unlock_weekly_calendar(), today_goal_setting('unlock'), dash.no_update]
    elif search == '?setting=True?usage': return [usage_weekly_calendar(), today_goal_setting('usage'), dash.no_update]
    elif search == '?setting=True?app': return [app_weekly_calendar(), today_goal_setting('app'), dash.no_update]
    elif search == '?setting=True':
        fig = today_goal_donut_plot()
        goal_graph = dcc.Graph(figure = fig, config={'displayModeBar': False}, className='calendar-donut' )
        return [dash.no_update, today_goal_setting(), goal_graph]
    elif (prev_clicks and int(key) > 1):
            return [get_calendar(int(key) -1), dash.no_update, dash.no_update]
    elif (next_clicks and int(key) < 12):
        return [get_calendar(int(key) + 1), dash.no_update, dash.no_update]
    else:
        return [dash.no_update, dash.no_update, dash.no_update]