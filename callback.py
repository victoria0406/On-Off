import dash
from dash.dependencies import Input, Output, State
from dash import html, dcc
from inputdata.goalsettingdata import usage_time_info, unlock_info, app_usage_info
from component.todaygoal import today_goal_setting, today_goal_donut_plot, unlock_weekly_calendar, usage_weekly_calendar, app_weekly_calendar
from component.calendar import get_calendar
import pandas as pd

app_usage_df = pd.read_csv('./datas/usage_time.csv')
def avg_app_usage(app):
    return app_usage_df[app].mean()

def selected_app_callback_factory():
    output = [Output('selected-app', 'children'), Output('avg-app-usage', 'children')],
    input = Input('app-dropdown', 'value'),
    def update_output(value):
        usage = avg_app_usage(value)
        return [[value, f'{usage // 60:.0f}h {usage % 60:.0f}m']]
    
    return [
        update_output,
        output,
        input,
    ]
    
plus_layout = html.Div([
'+'
], className="custom-checkbox plus")
minus_layout = html.Div([
    '-'
], className="custom-checkbox minus")
    
def usage_time_switch_callback_factory():
    output=[
        Output('goal-switch-output-usage-time', 'children'),
        Output('goal-switch-disable-usage-time-1', 'disabled'),
        Output('goal-switch-disable-usage-time-2', 'disabled'),
        Output('goal-setting-list-container-usage-time', 'className'),
    ]
    input=Input('goal-switch-input-usage-time', 'value')
    def update_output(value):
        if 'on' in value:
            usage_time_info['checked'] = True
            return [[plus_layout], False, False, 'goal-setting-list-container active']
        else:
            usage_time_info['checked'] = False
            return [[minus_layout], True, True, 'goal-setting-list-container']
        
    return [
        update_output,
        output,
        input,
    ]
    
def unlock_switch_callback_factory():
    output=[
        Output('goal-switch-output-unlock', 'children'),
        Output('goal-switch-disable-unlock-1', 'disabled'),
        Output('goal-setting-list-container-unlock', 'className'),
    ]
    input=Input('goal-switch-input-unlock', 'value')
    def update_output(value):
        if 'on' in value:
            unlock_info['checked'] = True
            return [[plus_layout], False, 'goal-setting-list-container active']
        else:
            unlock_info['checked'] = False
            return [[minus_layout], True, 'goal-setting-list-container']
        
    return [
        update_output,
        output,
        input,
    ]
    
def app_usage_switch_callback_factory():
    output=[
        Output('goal-switch-output-app-usage', 'children'),
        Output('app-dropdown', 'disabled'),
        Output('goal-switch-disable-app-usage-2', 'disabled'),
        Output('goal-switch-disable-app-usage-3', 'disabled'),
        Output('goal-setting-list-container-app-usage', 'className'),
    ]
    input=Input('goal-switch-input-app-usage', 'value')
    def update_output(value):
        if 'on' in value:
            app_usage_info['checked'] = True
            return [[plus_layout], False, False, False, 'goal-setting-list-container active']
        else:
            app_usage_info['checked'] = False
            return [[minus_layout], True, True, True, 'goal-setting-list-container']
        
    return [
        update_output,
        output,
        input,
    ]
    
def goal_confirm_callback_factory():
    output=Output('url', 'search')
    input = Input('goal-confirm-final', 'n_clicks')
    state = [
        State('goal-switch-disable-unlock-1', 'value'),
        State('goal-switch-disable-usage-time-1', 'value'),
        State('goal-switch-disable-usage-time-2', 'value'),
        State('app-dropdown', 'value'),
        State('goal-switch-disable-app-usage-2', 'value'),
        State('goal-switch-disable-app-usage-3', 'value'),
    ]
    def update_output(n_clicks, unlock_time, usage_hour, usage_minute, app_usage_app, app_usage_hour, app_usage_minute):
        if (n_clicks):
            unlock_info['time'] = unlock_time
            usage_time_info['hour'] = usage_hour
            usage_time_info['minute'] = usage_minute
            app_usage_info['app'] = app_usage_app
            app_usage_info['hour'] = app_usage_hour
            app_usage_info['minute'] = app_usage_minute
            return '?setting=True'
    return [
        update_output,
        output,
        input,
        state,
    ]

def goal_update_callback_factory():
    output=[Output('today-goal', 'children'), Output('today-goal-status', 'children')]
    input=Input('url', 'pathname')
    state=State('url', 'search')
    url_list=['?setting=True', '?setting=True?unlock', '?setting=True?usage', '?setting=True?app']
    def update_output(pathname, search):
        if pathname != '/goal' or not search in url_list: return [dash.no_update, dash.no_update]
        if search == url_list[1]: return [today_goal_setting('unlock'), dash.no_update]
        elif search == url_list[2]: return [today_goal_setting('usage'), dash.no_update]
        elif search == url_list[3]: return [today_goal_setting('app'), dash.no_update]
        elif search == url_list[0]: 
            fig = today_goal_donut_plot()
            goal_graph = dcc.Graph(figure = fig, config={'displayModeBar': False}, className='calendar-donut' )
            return [today_goal_setting(), goal_graph]
        else: return [today_goal_setting(), dash.no_update]
    return [
        update_output,
        output,
        input,
        state,
    ]

def goal_highlight_callback_factory():
    output=Output('calendar-container', 'children')
    input=[Input('url', 'pathname'), Input('prev-calender', 'n_clicks'), Input('next-calender', 'n_clicks')]
    state=[State('url', 'search'), State('month-title', 'key')]
    def update_output(pathname, prev_clicks, next_clicks, search, key):
        if pathname != '/goal': return dash.no_update
        elif search == '?setting=True?unlock': return unlock_weekly_calendar()
        elif search == '?setting=True?usage': return usage_weekly_calendar()
        elif search == '?setting=True?app': return app_weekly_calendar()
        elif (prev_clicks and int(key) > 1):
                return get_calendar(int(key) -1)
        elif (next_clicks and int(key) < 12):
            return get_calendar(int(key) + 1)
        else:
            return dash.no_update
    return [
        update_output,
        output,
        input,
        state,
    ]
    
def goal_update_sidebar_callback_factory():
    output=Output('goal-link', 'href')
    input=Input('url', 'pathname')
    state=State('url', 'search')
    def update_output(pathname, search):
        if pathname == '/goal' and search == '?setting=True':
            # print(pathname, search)
            return '/goal?setting=True'
        else:  return dash.no_update
    return [
        update_output,
        output,
        input,
        state,
    ]
def goal_setting_modal_callback_factory():
    output=[Output("modal", "is_open"), Output('modal-fault', 'is_open'), Output("goal-confirm", "n_clicks"), Output("close", "n_clicks"), Output("close-fault", "n_clicks")]
    input=[Input("goal-confirm", "n_clicks"), Input("close", "n_clicks"), Input("close-fault", "n_clicks")]
    state=[
        State("modal", "is_open"),
        State('modal-fault', 'is_open'),
        State('goal-switch-disable-unlock-1', 'value'),
        State('goal-switch-disable-usage-time-1', 'value'),
        State('goal-switch-disable-usage-time-2', 'value'),
        State('app-dropdown', 'value'),
        State('goal-switch-disable-app-usage-2', 'value'),
        State('goal-switch-disable-app-usage-3', 'value'),
    ]
    def update_output(n1, n2, n_fault, is_open, is_open_fault, unlock_time, usage_hour, usage_minute, app_usage_app, app_usage_hour, app_usage_minute):
        if (n2 or n_fault):
            return [False, False, 0, 0, 0]
        if (n1):
            if not (unlock_info['checked'] or usage_time_info['checked'] or app_usage_info['checked']):
                return [False, True, 0, 0, 0]
            if (unlock_info['checked'] and unlock_time == 0):
                return [False, True, 0, 0, 0]
            if (usage_time_info['checked'] and ((usage_hour == 0 and usage_minute == 0) or usage_hour == None or usage_minute == None)):
                return [False, True, 0, 0, 0]
            if (app_usage_info['checked'] and app_usage_app == None):
                return [False, True, 0, 0, 0]
            if (app_usage_info['checked'] and ((app_usage_hour == 0 and app_usage_minute == 0) or app_usage_hour == None or app_usage_minute == None)):
                return [False, True, 0, 0, 0]
            unlock_info['time'] = unlock_time
            usage_time_info['hour'] = usage_hour
            usage_time_info['minute'] = usage_minute
            app_usage_info['app'] = app_usage_app
            app_usage_info['hour'] = app_usage_hour
            app_usage_info['minute'] = app_usage_minute
            return [True, False, 0, 0, 0]
        else:
            return [False, False, 0, 0, 0]
    return [
        update_output,
        output,
        input,
        state,
    ]
def update_mention_header_callback_factory():
    output = Output('header-mention', 'children')
    input=Input('url', 'pathname')
    def update_output(pathname):
        if pathname == '/goal' or pathname == '/goal/setting':
            return 'Set goal to use your phone well!'
        elif pathname == '/report/group':
            return 'Compare your usage with others :)'
        elif pathname == '/report/weekly':
            return 'Let’s check your phone usage this week!'
        elif pathname == '/report':
            return 'Let’s check your phone usage today!'
        else : return 'Hello'
    return [
        update_output,
        output,
        input,
    ]
    
def get_callbacks():
    return [
        selected_app_callback_factory(),
        usage_time_switch_callback_factory(),
        unlock_switch_callback_factory(),
        app_usage_switch_callback_factory(),
        goal_update_callback_factory(),
        goal_update_sidebar_callback_factory(),
        goal_highlight_callback_factory(),
        goal_setting_modal_callback_factory(),
        update_mention_header_callback_factory(),
    ]