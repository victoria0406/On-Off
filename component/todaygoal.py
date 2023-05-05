import dash
from dash.dependencies import Input, Output, State
from dash import html, dcc
from inputdata.goalsettingdata import usage_time_info, unlock_info, app_usage_info
from component.goaldonutplot import goal_donut_plot
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
    return component;

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
    return component;

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
    return component;

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

def today_goal_setting(highlighted=None):
    return_children = [html.P('Today Goal', style={'font-weight': 'bold'})]
    print(get_goal_info())
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
    
today_goal_not_setting = [
    html.P('Today Goal', style={'font-weight': 'bold'}),
    html.A('+', className='set-goal-button',href='/goalsetting'),
    html.P('Set Your Goal!', style={'margin-bottom': '120px'})
]