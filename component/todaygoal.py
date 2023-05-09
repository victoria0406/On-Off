import dash
import datetime as dt
import pandas as pd
from dash.dependencies import Input, Output, State
from dash import html, dcc
from inputdata.goalsettingdata import usage_time_info, unlock_info, app_usage_info
from component.goaldonutplot import goal_donut_plot, week_donut_plot
from component.graph import usage_graph, unlock_graph, app_usage_graph
import pandas as pd

today_day = 10

app_usage_df = pd.read_csv('./datas/app_usage_time.csv')
app_usage_df['day'] = pd.to_datetime(app_usage_df['date']).dt.day
unlock_df = pd.read_csv('./datas/unlock.csv')
unlock_df['day'] = pd.to_datetime(unlock_df['date']).dt.day

today_df = app_usage_df[app_usage_df['day'] == today_day]
total_usage = today_df['Total'].values[0]
app_usage = today_df[app_usage_info['app']].values[0]
unlock = unlock_df[unlock_df['day'] == today_day]['unlock'].values[0]


def unlock_component(highlighted=None):
    data = unlock;
    component = html.Div([
        html.P('Unlocks', className='goal-title'),
        html.A([
            html.Div([], className='goal-state-check'),
            html.Span(f"{data} / {unlock_info['time']} times ({(data / unlock_info['time'] * 100):.1f}%)")
        ], className='goal-list unlock', href='/goal?setting=True' if (highlighted == 'unlock') else '/goal?setting=True?unlock')
    ])
    return component

def usage_time_component(highlighted=None):
    data = round(float(total_usage) / 60, 1);
    usage_time = usage_time_info['hour'] + usage_time_info['minite'] / 60
    component = html.Div([
        html.P('Usage Time',className='goal-title'),
        html.A([
            html.Div([], className='goal-state-check'),
            html.Span(f"{data} / {usage_time} h ({(data / usage_time * 100):.1f}%)")
        ], className='goal-list usage', href='/goal?setting=True' if (highlighted == 'usage') else '/goal?setting=True?usage')
    ])
    return component

def app_usage_component(highlighted=None):
    data = round(float(app_usage) / 60, 1);
    usage_time = app_usage_info['hour'] + app_usage_info['minite'] / 60
    component = html.Div([
        html.P(f"App Usage Time for {app_usage_info['app']}",className='goal-title'),
        html.A([
            html.Div([], className='goal-state-check'),
            html.Span(f"{data} / {usage_time} h ({(data / usage_time * 100):.1f}%)")
        ], className='goal-list app', href='/goal?setting=True' if (highlighted == 'app') else '/goal?setting=True?app')
    ])
    return component

def get_goal_info():
    return_data = [None, None, None];
    if (unlock_info['checked']):
        exceed = max(unlock - unlock_info['time'], 0)
        real = max(min(unlock, 2 * unlock_info['time'] - unlock), 0)
        goal = max(0, unlock_info['time']-unlock)
        return_data[0] = [exceed, real, goal]
    if (usage_time_info['checked']):
        usage_by_m = usage_time_info['hour'] * 60 + usage_time_info['minite'];
        exceed = max(total_usage - usage_by_m, 0)
        real = max(0, min(total_usage, 2 * usage_by_m - total_usage))
        goal = max(0, usage_by_m-total_usage)
        return_data[1] = [exceed, real, goal]
    if (app_usage_info['checked']):
        app_usage_by_m = app_usage_info['hour'] * 60 + app_usage_info['minite'];
        exceed = max(app_usage - app_usage_by_m, 0)
        real = max(0, min(app_usage, 2 * app_usage_by_m - app_usage))
        goal = max(0, app_usage_by_m-app_usage)
        return_data[2] = [exceed, real, goal]
        
    return return_data
def today_goal_donut_plot(highlighted = None):
    fig = goal_donut_plot(*get_goal_info(), highlighted)
    return fig

def today_goal_setting(highlighted=None):
    return_children = [html.P('Today Goal', style={'font-weight': 'bold'})]
    fig = today_goal_donut_plot(highlighted)
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

def get_calendar_donut_plot(day, index):
    goal_state = get_goal_state(day)
    if goal_state == None : return None
    fig = week_donut_plot(goal_state[index], index)
    donut = dcc.Graph(figure = fig, config={'displayModeBar': False}, className='calendar-donut')
    return donut


def unlock_weekly_calendar(highlighted=None):
    today_day = dt.datetime(2023, 5, 10)
    date_list = [today_day - dt.timedelta(days=x) for x in range(7)]
    date_list.reverse()
    
    table = html.Table(className=f'weekly-calendar', children=[
        html.Thead(children=[
            html.Tr(children=[
                html.Th(str(day.month)+"/"+str(day.day), 
                        style={'color': '#FF6F66'} if (day.weekday() == 6) else ({'color': '#FDB03D'} if (day.weekday() == 5) else {}))
                for day in date_list
            ])
        ]),
        html.Tbody(children=[
            html.Tr(children=[
                html.Td(children=[
                    get_calendar_donut_plot(day.day, 0)
                ], className='today' if (day == today_day) else '' ) if day != 0 else html.Td('')
                for day in date_list
            ])
        ])
    ])
    
    return_children = [
        html.Div(children=[
            html.Div([html.P('Your Weekly - Unlock', className='weekly-calendar-title'), table],
                     className='weekly-calendar-container',),
            html.Div(children=[
                html.P('Unlock', style={'font-size': '20px'}),
                html.Div(dcc.Graph(figure = unlock_graph(), config={'displayModeBar': False}),style={'margin-top':'-50px'})
            ])
        ])
    ]
    component = html.Div(return_children, className='week-calendar')
    return component

def usage_weekly_calendar(highlighted=None):
    today_day = dt.datetime(2023, 5, 10)
    date_list = [today_day - dt.timedelta(days=x) for x in range(7)]
    date_list.reverse()
    
    table = html.Table(className=f'weekly-calendar', children=[
        html.Thead(children=[
            html.Tr(children=[
                html.Th(str(day.month)+"/"+str(day.day), 
                        style={'color': '#FF6F66'} if (day.weekday() == 6) else ({'color': '#FDB03D'} if (day.weekday() == 5) else {}))
                for day in date_list
            ])
        ]),
        html.Tbody(children=[
            html.Tr(children=[
                html.Td(children=[
                    get_calendar_donut_plot(day.day, 1)
                ], className='today' if (day == today_day) else '' ) if day != 0 else html.Td('')
                for day in date_list
            ])
        ])
    ])
    
    return_children = [
        html.Div(children=[
            html.Div([html.P('Your Weekly - Usage Time', className='weekly-calendar-title'), table],
                     className='weekly-calendar-container',),
            html.Div(children=[
                html.P('Usage Time', style={'font-size': '20px'}),
                html.Div(dcc.Graph(figure = usage_graph(), config={'displayModeBar': False})),
            ])
        ])
    ]
    component = html.Div(return_children, className='week-calendar')
    return component

def app_weekly_calendar(highlighted=None):
    today_day = dt.datetime(2023, 5, 10)
    date_list = [today_day - dt.timedelta(days=x) for x in range(7)]
    date_list.reverse()
    
    table = html.Table(className=f'weekly-calendar', children=[
        html.Thead(children=[
            html.Tr(children=[
                html.Th(str(day.month)+"/"+str(day.day), 
                        style={'color': '#FF6F66'} if (day.weekday() == 6) else ({'color': '#FDB03D'} if (day.weekday() == 5) else {}))
                for day in date_list
            ])
        ]),
        html.Tbody(children=[
            html.Tr(children=[
                html.Td(children=[
                    get_calendar_donut_plot(day.day, 2)
                ], className='today' if (day == today_day) else '' ) if day != 0 else html.Td('')
                for day in date_list
            ])
        ])
    ])
    
    return_children = [
        html.Div(children=[
            html.Div([html.P('Your Weekly - App Usage Time', className='weekly-calendar-title'), table],
                     className='weekly-calendar-container',),
            html.Div(children=[
                html.P('App Usage', style={'font-size': '20px'}),
                html.Div(dcc.Graph(figure = app_usage_graph(), config={'displayModeBar': False})),
            ])
        ])
    ]
    component = html.Div(return_children, className='week-calendar')
    return component

today_goal_not_setting = [
    html.P('Today Goal', style={'font-weight': 'bold'}),
    html.A('+', className='set-goal-button',href='/goalsetting'),
    html.P('Set Your Goal!', style={'margin-bottom': '120px'})
]