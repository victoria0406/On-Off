import dash
import datetime as dt
import pandas as pd
from dash.dependencies import Input, Output, State
from dash import html, dcc
from inputdata.goalsettingdata import usage_time_info, unlock_info, app_usage_info, is_goal_setted
from component.goaldonutplot import goal_donut_plot, week_donut_plot
from component.graph import usage_graph, unlock_graph, app_usage_graph


def unlock_component(highlighted=None):
    data = 4
    component = html.Div([
        html.P('Unlocks', className='goal-title'),
        html.A([
            html.Div([], className='goal-state-check'),
            html.Span(f"{data} / {unlock_info['time']} times ({(data / unlock_info['time']):.1f}%)")
        ], className='goal-list unlock', href='/goal?setting=True' if (highlighted == 'unlock') else '/goal?setting=True?unlock')
    ])
    return component

def usage_time_component(highlighted=None):
    data = 2
    usage_time = usage_time_info['hour'] + usage_time_info['minite'] / 60
    component = html.Div([
        html.P('Usage Time',className='goal-title'),
        html.A([
            html.Div([], className='goal-state-check'),
            html.Span(f"{data} / {usage_time} h ({(data / usage_time):.1f}%)")
        ], className='goal-list usage', href='/goal?setting=True' if (highlighted == 'usage') else '/goal?setting=True?usage')
    ])
    return component

def app_usage_component(highlighted=None):
    data = 1
    usage_time = app_usage_info['hour'] + app_usage_info['minite'] / 60
    component = html.Div([
        html.P(f"App Usage Time for {app_usage_info['app']}",className='goal-title'),
        html.A([
            html.Div([], className='goal-state-check'),
            html.Span(f"{data} / {usage_time} h ({(data / usage_time):.1f}%)")
        ], className='goal-list app', href='/goal?setting=True' if (highlighted == 'app') else '/goal?setting=True?app')
    ])
    return component

def get_goal_info():
    return [
        [0, 4, unlock_info['time']-4] if unlock_info['checked'] else None,
        [0, 2, usage_time_info['hour'] + usage_time_info['minite'] / 60 - 2] if usage_time_info['checked'] else None,
        [0, 1, app_usage_info['hour'] + app_usage_info['minite'] / 60 - 1] if app_usage_info['checked'] else None,
    ]

def today_goal_setting(highlighted=None):
    return_children = [html.P('Today Goal', style={'font-weight': 'bold'})]
    fig = goal_donut_plot(*get_goal_info(), highlighted)
    return_children.append(dcc.Graph(figure = fig, config={'displayModeBar': False}, className='today-goal-fig'))
    if unlock_info['checked']:
        return_children.append(unlock_component(highlighted))
    if usage_time_info['checked']:
        return_children.append(usage_time_component(highlighted))
    if app_usage_info['checked']:
        return_children.append(app_usage_component(highlighted))
    component = html.Div(return_children, className='today-goal-list')
    return component

goal_states_df= pd.read_csv('./datas/goal_states.csv')
goal_states_df['day'] = pd.to_datetime(goal_states_df['date']).dt.day

def get_goal_state(day):
    day_goal_state = goal_states_df[goal_states_df['day'] == day]
    return_data = [None, None, None]
    if day_goal_state.size == 0 : return None
    day_goal_state = day_goal_state.fillna(-1, axis=1)
    if (day_goal_state['unlock_real'].values[0] > 0):
        exceed = max(day_goal_state['unlock_real'].values[0]-day_goal_state['unlock_goal'].values[0], 0)
        real = min(day_goal_state['unlock_real'].values[0], day_goal_state['unlock_goal'].values[0])
        goal = max(0, day_goal_state['unlock_goal'].values[0] - day_goal_state['unlock_real'].values[0])
        return_data[0] = [exceed, real, goal]
    if (day_goal_state['total_usage_real'].values[0] > 0):
        exceed = max(day_goal_state['total_usage_real'].values[0]-day_goal_state['total_usage_goal'].values[0], 0)
        real = min(day_goal_state['total_usage_real'].values[0], day_goal_state['total_usage_goal'].values[0])
        goal = max(0, day_goal_state['total_usage_goal'].values[0] - day_goal_state['total_usage_real'].values[0])
        return_data[1] = [exceed, real, goal]
    if (day_goal_state['app_usage_real'].values[0] > 0):
        exceed = max(day_goal_state['app_usage_real'].values[0]-day_goal_state['app_usage_goal'].values[0], 0)
        real = min(day_goal_state['app_usage_real'].values[0], day_goal_state['app_usage_goal'].values[0])
        goal = max(0, day_goal_state['app_usage_goal'].values[0] - day_goal_state['app_usage_real'].values[0])
        return_data[2] = [exceed, real, goal]
    return return_data

def get_calender_donut_plot(day, index):
    goal_state = get_goal_state(day)
    if goal_state == None : return None
    fig = week_donut_plot(goal_state[index], index)
    donut = dcc.Graph(figure = fig, config={'displayModeBar': False}, className='calender-donut')
    return donut

def unlock_weekly_calender(highlighted=None):
    today_day = dt.datetime(2023, 5, 10)
    week_ago = today_day - dt.timedelta(days=7)
    today_day = today_day.day
    week_ago = week_ago.day
    
    table = html.Table(className=f'goal-calender', children=[
        html.Thead(children=[
            html.Tr(children=[
                html.Th('Sun'), html.Th('Mon'), html.Th('Tue'),
                html.Th('Wed'), html.Th('Thr'), html.Th('Fri'),
                html.Th('Sat')
            ])
        ]),
        html.Tbody(children=[
            html.Tr(children=[
                html.Td(children=[
                    str(day),
                    get_calender_donut_plot(day, 0)
                ], className='today' if (day == today_day) else '' ) if day != 0 else html.Td('')
                for day in range(week_ago+1, today_day+1)
            ])
        ])
    ])
    
    return_children = [
        html.Div(children=[
            html.Div(['Your Weekly - Unlock', table],
                     className='weekly-calander-container',),
            html.Div(children=[
                html.P('Unlock'),
                html.Div(dcc.Graph(figure = unlock_graph(), config={'displayModeBar': False}),style={'margin-top':'-50px'})
            ])
        ])
    ]
    component = html.Div(return_children, className='week-calender')
    return component

def usage_weekly_calender(highlighted=None):
    today_day = dt.datetime(2023, 5, 10)
    week_ago = today_day - dt.timedelta(days=7)
    today_day = today_day.day
    week_ago = week_ago.day
    
    table = html.Table(className=f'goal-calender', children=[
        html.Thead(children=[
            html.Tr(children=[
                html.Th('Sun'), html.Th('Mon'), html.Th('Tue'),
                html.Th('Wed'), html.Th('Thr'), html.Th('Fri'),
                html.Th('Sat')
            ])
        ]),
        html.Tbody(children=[
            html.Tr(children=[
                html.Td(children=[
                    str(day),
                    get_calender_donut_plot(day, 1)
                ], className='today' if (day == today_day) else '' ) if day != 0 else html.Td('')
                for day in range(week_ago+1, today_day+1)
            ])
        ])
    ])
    
    return_children = [
        html.Div(children=[
            html.Div(['Your Weekly - Usage Time', table],
                     className='weekly-calander-container',),
            html.Div(children=[
                html.P('Usage Time'),
                html.Div(dcc.Graph(figure = usage_graph(), config={'displayModeBar': False})),
            ])
        ])
    ]
    component = html.Div(return_children, className='week-calender')
    return component

def app_weekly_calender(highlighted=None):
    today_day = dt.datetime(2023, 5, 10)
    week_ago = today_day - dt.timedelta(days=7)
    today_day = today_day.day
    week_ago = week_ago.day
    
    table = html.Table(className=f'goal-calender', children=[
        html.Thead(children=[
            html.Tr(children=[
                html.Th('Sun'), html.Th('Mon'), html.Th('Tue'),
                html.Th('Wed'), html.Th('Thr'), html.Th('Fri'),
                html.Th('Sat')
            ])
        ]),
        html.Tbody(children=[
            html.Tr(children=[
                html.Td(children=[
                    str(day),
                    get_calender_donut_plot(day, 2)
                ], className='today' if (day == today_day) else '' ) if day != 0 else html.Td('')
                for day in range(week_ago+1, today_day+1)
            ])
        ])
    ])
    
    return_children = [
        html.Div(children=[
            html.Div(['Your Weekly - App Usage', table],
                     className='weekly-calander-container',),
            html.Div(children=[
                html.P('App Usage'),
                html.Div(dcc.Graph(figure = app_usage_graph(), config={'displayModeBar': False})),

            ])
        ])
    ]
    component = html.Div(return_children, className='week-calender')
    return component

today_goal_not_setting = [
    html.P('Today Goal', style={'font-weight': 'bold'}),
    html.A('+', className='set-goal-button',href='/goalsetting'),
    html.P('Set Your Goal!', style={'margin-bottom': '120px'})
]